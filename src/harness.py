#!/usr/bin/env python3
"""Minimal Home Assistant blueprint harness: renders variables + drawcustom payload with
stubbed HA template functions, then renders the payload with odl-renderer to a PNG.

usage: harness.py blueprint.yaml scenario.py out.png
scenario.py defines: INPUTS (dict), STATES (dict entity -> {'state':..., 'attributes':{...}, 'last_updated': dt}),
NOW (datetime, tz-aware), optional CALENDAR (dict entity -> list of events), FORECASTS (dict entity -> {'hourly':[...], 'daily':[...]}),
TRIGGER (dict), ACCENT ('red'|'yellow')
"""
import os, sys, ast, json, math, re, asyncio, datetime as dt, importlib.util
os.environ.setdefault('EP_ROOT', os.path.dirname(os.path.abspath(__file__)))   # scenarios load each other from <root>/scen
import yaml
import jinja2
from jinja2.sandbox import ImmutableSandboxedEnvironment

TZ = dt.timezone(dt.timedelta(hours=1))


class Input:
    def __init__(self, name): self.name = name
    def __repr__(self): return f"!input {self.name}"


class Loader(yaml.SafeLoader):
    pass


Loader.add_constructor('!input', lambda l, n: Input(l.construct_scalar(n)))


def load_bp(path):
    with open(path, encoding='utf-8') as f:
        return yaml.load(f, Loader=Loader)


def collect_defaults(inputs, out):
    for k, v in (inputs or {}).items():
        if isinstance(v, dict) and 'input' in v and 'selector' not in v:
            collect_defaults(v['input'], out)
        elif isinstance(v, dict):
            if 'default' in v:
                out[k] = v.get('default')
            else:  # a required input: the scenario gives it; one it leaves out is empty (a list where several are picked)
                out[k] = [] if ((v.get('selector') or {}).get('entity') or {}).get('multiple') else ''
    return out


def subst(obj, vals):
    if isinstance(obj, Input):
        return vals[obj.name]
    if isinstance(obj, dict):
        return {k: subst(v, vals) for k, v in obj.items()}
    if isinstance(obj, list):
        return [subst(v, vals) for v in obj]
    return obj


def _bytecode_cache():
    """compiled templates, kept between renders and processes: a render no longer compiles ep_design.jinja again. Each
    template is kept by its file and checked against its source, so a changed file is compiled again on its own.
    EP_NOCACHE=1 compiles every time."""
    import tempfile
    if os.environ.get('EP_NOCACHE'):
        return None
    d = os.path.join(tempfile.gettempdir(), 'epaper_jinja_cache')
    os.makedirs(d, exist_ok=True)
    return jinja2.FileSystemBytecodeCache(d)


def require_raqm():
    """without Raqm Pillow applies no kerning and text renders up to 1 px wider than the devices draw it"""
    from PIL import features
    if not features.check('raqm'):
        sys.exit('Pillow has no Raqm (brew install fribidi, then reinstall Pillow): renders would not match the devices')


def make_env(sc):
    require_raqm()
    ct = os.environ.get('EP_CT')  # a config/custom_templates folder, for blueprints that import macros
    env = ImmutableSandboxedEnvironment(extensions=['jinja2.ext.loopcontrols', 'jinja2.ext.do'], undefined=jinja2.ChainableUndefined,
                                        loader=jinja2.FileSystemLoader(ct) if ct else None, bytecode_cache=_bytecode_cache())

    def as_function(macro):  # Home Assistant's as_function filter
        def wrapper(*args, **kwargs):
            rv = None

            def returns(value):
                nonlocal rv
                rv = value
                return value
            macro(*args, **kwargs, returns=returns)
            return rv
        return wrapper
    env.filters['as_function'] = as_function
    env.policies['json.dumps_kwargs'] = {'ensure_ascii': False, 'sort_keys': False}
    states = sc.STATES
    now_v = sc.NOW

    def _st(e):
        return states.get(e)

    class SObj:
        def __init__(self, eid, d):
            self.entity_id = eid; self.state = d['state']; self.attributes = d.get('attributes') or {}
            self.last_updated = d.get('last_updated', now_v); self.last_changed = d.get('last_changed', self.last_updated)
            if 'last_reported' in d: self.last_reported = d['last_reported']
            self.name = self.attributes.get('friendly_name', eid)
            self.domain = eid.split('.')[0]

    def g_states(e, *a, **k):
        s = _st(e)
        return s['state'] if s else 'unknown'

    def g_expand(*ents):
        out = []
        for e in ents:
            for x in (e if isinstance(e, (list, tuple)) else [e]):
                if x in states:
                    out.append(SObj(x, states[x]))
        return out

    def g_state_attr(e, a):
        s = _st(e)
        return (s.get('attributes') or {}).get(a) if s else None

    def g_is_state(e, v):
        return g_states(e) == v

    def g_now():
        return now_v

    def to_float(v, default=jinja2.Undefined):
        try:
            return float(v)
        except Exception:
            if default is not jinja2.Undefined:
                return default
            raise ValueError(f"float() got invalid input {v!r}")

    def to_int(v, default=0, base=10):
        try:
            if isinstance(v, str):
                return int(float(v))
            return int(v)
        except Exception:
            return default

    def as_timestamp(v, default=None):
        try:
            if isinstance(v, (int, float)):
                return float(v)
            if isinstance(v, dt.datetime):
                return v.timestamp()
            if isinstance(v, str):
                d = dt.datetime.fromisoformat(v.replace('Z', '+00:00'))
                if d.tzinfo is None:
                    d = d.replace(tzinfo=TZ)
                return d.timestamp()
        except Exception:
            return default
        return default

    def timestamp_custom(ts, fmt='%Y-%m-%d %H:%M:%S', local=True, default=None):
        try:
            d = dt.datetime.fromtimestamp(float(ts), TZ)
            return d.strftime(fmt)
        except Exception:
            return default

    def as_datetime(v, default=None):
        try:
            if isinstance(v, dt.datetime):
                return v
            if isinstance(v, (int, float)):
                return dt.datetime.fromtimestamp(v, dt.timezone.utc)
            d = dt.datetime.fromisoformat(str(v).replace('Z', '+00:00'))
            return d if d.tzinfo else d.replace(tzinfo=TZ)
        except Exception:
            return default

    def as_local(d):
        return d.astimezone(TZ)

    def today_at(s='00:00'):
        h, m = [int(x) for x in s.split(':')[:2]]
        return now_v.replace(hour=h, minute=m, second=0, microsecond=0)

    def ha_round(v, prec=0, method='common', default=None):
        try:
            v = float(v)
        except Exception:
            return default
        if method == 'ceil':
            r = math.ceil(v * 10 ** prec) / 10 ** prec
        elif method == 'floor':
            r = math.floor(v * 10 ** prec) / 10 ** prec
        else:
            r = round(v, prec) if method != 'half' else round(v * 2) / 2
        return int(r) if prec == 0 else r

    def ha_log(v, base=math.e, default=None):
        try:
            return math.log(float(v), float(base))
        except Exception:
            return default

    def regex_replace(v, find='', replace='', ignorecase=False):
        return re.sub(find, replace, str(v), flags=re.I if ignorecase else 0)

    def regex_match(v, find='', ignorecase=False):
        return bool(re.match(find, str(v), flags=re.I if ignorecase else 0))

    def regex_search(v, find='', ignorecase=False):
        return bool(re.search(find, str(v), flags=re.I if ignorecase else 0))

    def integration_entities(name):
        return [e for e, s in states.items() if s.get('integration') == name]

    def device_id(e):
        return states.get(e, {}).get('device_id')

    def device_attr(d, attr):
        return getattr(sc, 'MODELS', {}).get(d, '3.5" BWR') if attr == 'model' else None

    # HA 2026.11 naming: a scenario's DEVICE_NAMES maps entity -> device name; the entity name is the
    # friendly name minus that prefix ('' for a device's main entity), or the whole friendly name without a device
    def device_name(e):
        return getattr(sc, 'DEVICE_NAMES', {}).get(e)

    def entity_name(e):
        s = _st(e)
        fn = ((s or {}).get('attributes') or {}).get('friendly_name', e if s else None)
        dn = device_name(e)
        if fn and dn and fn.startswith(dn):
            return fn[len(dn):].strip()
        return fn

    def iif(c, a=True, b=False, n=None):
        return a if c else b

    class StatesFn:  # states('x') and iteration over all state objects, like HA's states
        def __call__(self, e, *a, **k):
            return g_states(e, *a, **k)

        def __iter__(self):
            return iter([SObj(e, d) for e, d in states.items()])
    env.globals.update(expand=g_expand, states=StatesFn(), state_attr=g_state_attr, is_state=g_is_state, now=g_now,
                       as_timestamp=as_timestamp, as_datetime=as_datetime, as_local=as_local,
                       today_at=today_at, timedelta=dt.timedelta, float=to_float, int=to_int,
                       integration_entities=integration_entities, device_id=device_id, iif=iif, device_attr=device_attr,
                       strptime=lambda v, f, *d: dt.datetime.strptime(v, f), state_translated=lambda e: getattr(sc, 'TRANSLATED', {}).get(e, g_states(e)), namespace=jinja2.utils.Namespace, area_name=lambda e: getattr(sc, 'AREAS', {}).get(e), device_name=device_name, entity_name=entity_name, min=min, max=max, range=range)
    env.filters.update(float=to_float, int=to_int, as_timestamp=as_timestamp,
                       timestamp_custom=timestamp_custom, expand=lambda e: g_expand(e), as_datetime=as_datetime, as_local=as_local,
                       round=ha_round, log=ha_log, regex_replace=regex_replace, regex_match=regex_match,
                       regex_search=regex_search, iif=iif, device_id=device_id, bitwise_and=lambda a, b: int(a) & int(b), is_number=lambda v: isinstance(v, (int, float)) or bool(re.fullmatch(r'-?\d+(\.\d+)?', str(v))),
                       tojson=lambda v, indent=None: json.dumps(v, ensure_ascii=False, indent=indent),
                       to_json=lambda v, **k: json.dumps(v, ensure_ascii=False))
    env.filters.update(cos=lambda v: math.cos(float(v)), sin=lambda v: math.sin(float(v)), acos=lambda v: math.acos(float(v)))
    env.globals['pi'] = math.pi
    env.globals['atan2'] = lambda y, x: math.atan2(float(y), float(x))
    env.filters['sqrt'] = lambda v: math.sqrt(float(v))
    env.filters['bool'] = lambda v, d=None: v if isinstance(v, bool) else (str(v).strip().lower() in ('true', 'yes', 'on', '1'))
    env.tests['match'] = lambda v, p: bool(re.match(p, str(v)))
    env.tests['search'] = lambda v, p: bool(re.search(p, str(v)))
    env.tests['is_number'] = lambda v: isinstance(v, (int, float)) or bool(re.fullmatch(r'-?\d+(\.\d+)?', str(v)))
    env.filters['is_number'] = env.tests['is_number']
    env.tests['datetime'] = lambda v: isinstance(v, dt.datetime)
    return env


def parse_result(s):
    st = s.strip()
    try:
        v = ast.literal_eval(st)
        if isinstance(v, (str,)) and not (st.startswith(("'", '"'))):
            return st
        return v
    except Exception:
        if st == 'True': return True
        if st == 'False': return False
        return st


def render_value(env, tmpl, ctx):
    if isinstance(tmpl, str) and ('{{' in tmpl or '{%' in tmpl):
        out = env.from_string(tmpl).render(**ctx)
        return parse_result(out)
    if isinstance(tmpl, dict):
        return {k: render_value(env, v, ctx) for k, v in tmpl.items()}
    if isinstance(tmpl, list):
        return [render_value(env, v, ctx) for v in tmpl]
    if isinstance(tmpl, str):               # Home Assistant parses a static text like a template's result: '863651' is a number
        return parse_result(tmpl)
    return tmpl


def canvas_of(bp_path):
    """the canvas of the blueprint's layout (lib/layouts.py): a scenario doesn't carry a size"""
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lib'))
    from layouts import layouts
    name = os.path.basename(bp_path)
    for l in layouts():
        if l['blueprint'] == name:
            return l['canvas']
    raise SystemExit(f'{name}: no layout draws this blueprint, and the scenario sets no SIZE')


# what the last run did besides drawing: the LED calls' devices and the template triggers that fire in the scenario's state
LAST = {'led': [], 'fired': []}


class NoDraw(SystemExit):
    """the automation stopped at a condition before it drew anything, as Home Assistant stops it"""


def run(bp_path, sc_path, out_png, choose_index=None):
    spec = importlib.util.spec_from_file_location('sc', sc_path)
    sc = importlib.util.module_from_spec(spec); spec.loader.exec_module(sc)
    bp = load_bp(bp_path)
    vals = collect_defaults(bp['blueprint']['input'], {})
    vals.update(getattr(sc, 'INPUTS', {}))
    doc = subst({k: v for k, v in bp.items() if k != 'blueprint'}, vals)
    env = make_env(sc)
    ctx = {'trigger': getattr(sc, 'TRIGGER', {'platform': 'time_pattern', 'entity_id': None})}
    ctx.update(getattr(sc, 'EXTRA_CTX', {}))
    # the template triggers, evaluated with the trigger variables in the scenario's state: which of them fire now
    LAST['led'], LAST['fired'] = [], []
    tctx = {k: render_value(env, v, {}) for k, v in (doc.get('trigger_variables') or {}).items()}
    for t in doc.get('trigger') or doc.get('triggers') or []:
        if isinstance(t, dict) and t.get('trigger', t.get('platform')) == 'template' and \
                render_value(env, t['value_template'], dict(tctx)) in (True, 'True', 'true'):
            LAST['fired'].append(t.get('id'))
    over = getattr(sc, 'OVERRIDE', {})       # a scenario may fix a blueprint variable (ds_set: another release's blueprint)
    for k, v in (doc.get('variables') or {}).items():
        ctx[k] = over[k] if k in over else render_value(env, v, ctx)
    steps = doc.get('action') or doc.get('actions')
    calls = []

    def walk(steps):
        for st in steps:
            if 'variables' in st:
                for k, v in st['variables'].items():
                    try:
                        ctx[k] = render_value(env, v, ctx)
                    except Exception as ex:
                        raise SystemExit(f'variable {k} failed: {ex!r}')
            elif st.get('condition') == 'template':       # a condition step: false stops the automation here
                if render_value(env, st['value_template'], ctx) not in (True, 'True', 'true'):
                    raise NoDraw('the automation stops at a condition: nothing is drawn')
            elif 'choose' in st:
                done = False
                for opt in st['choose']:
                    conds = opt.get('conditions', [])
                    conds = conds if isinstance(conds, list) else [conds]
                    # a condition is a template string, or Home Assistant's {condition: template, value_template: ...}
                    ok = all(render_value(env, c if isinstance(c, str) else c['value_template'], ctx) in (True, 'True', 'true')
                             if isinstance(c, str) or (isinstance(c, dict) and c.get('condition') == 'template') else True for c in conds)
                    if ok:
                        walk(opt['sequence']); done = True; break
                if not done and 'default' in st:
                    walk(st['default'])
            elif 'if' in st:
                conds = st['if'] if isinstance(st['if'], list) else [st['if']]
                ok = all(render_value(env, c if isinstance(c, str) else c['value_template'], ctx) in (True, 'True', 'true')
                         for c in conds if isinstance(c, str) or (isinstance(c, dict) and c.get('condition') == 'template'))
                walk(st['then'] if ok else st.get('else', []))
            elif st.get('action') == 'opendisplay.activate_led':
                LAST['led'].append(render_value(env, st['data']['device_id'], ctx))
            elif st.get('action') in ('opendisplay.drawcustom',):
                calls.append(render_value(env, st['data'], ctx))
            elif 'action' in st and st['action'].startswith('calendar.get_events'):
                ctx[st['response_variable']] = sc.CALENDAR_RESPONSE
            elif st.get('action') == 'todo.get_items':
                ctx[st['response_variable']] = getattr(sc, 'TODO_RESPONSE', {})
            elif st.get('action') == 'energyzero.get_energy_prices':
                ctx[st['response_variable']] = getattr(sc, 'PRICE_RESPONSE', {})
            elif 'action' in st and st['action'] == 'recorder.get_statistics':
                ctx[st['response_variable']] = getattr(sc, 'STATS_RESPONSE', {'statistics': {}})
            elif 'action' in st and st['action'].startswith('weather.get_forecasts'):
                typ = st['data']['type']
                ctx[st['response_variable']] = {e: {'forecast': sc.FORECASTS[e][typ]} for e in sc.FORECASTS}
            elif 'service' in st and str(st['service']).startswith('weather.get_forecasts'):
                typ = st['data']['type']
                ctx[st['response_variable']] = {e: {'forecast': sc.FORECASTS[e][typ]} for e in sc.FORECASTS}
            elif 'repeat' in st or 'delay' in st or 'wait_template' in st:
                pass
            else:
                pass
    walk(steps)
    if not calls:
        raise SystemExit('no drawcustom call reached')
    data = calls[-1]
    payload = data['payload']
    if isinstance(payload, str):
        raise SystemExit('payload did not parse to a list:\n' + payload[:3000])
    if getattr(sc, 'MASK_SET', None):       # the templates' set id changes with every template change: a case that shows
        ct = os.environ.get('EP_CT')        # it draws a fixed one instead, so its render only changes with the drawing
        m = re.search(r"EP_SET = '([0-9a-z]+)'", open(os.path.join(ct, 'ep_design.jinja'), encoding='utf-8').read()) if ct else None
        if m:
            for e in payload:
                if isinstance(e.get('value'), str):
                    e['value'] = e['value'].replace(m.group(1).upper(), sc.MASK_SET)
    from odl_renderer import generate_image
    W, H = getattr(sc, 'SIZE', None) or canvas_of(bp_path)
    img = asyncio.run(generate_image(width=W, height=H, elements=payload, background=data.get('background', 'white'),
                                     accent_color=getattr(sc, 'ACCENT', 'red'), font_dirs=[os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fonts')]))
    img.save(out_png)
    print(f"ok: {len(payload)} elements, dither={data.get('dither')}, rotate={data.get('rotate')}")
    return payload


if __name__ == '__main__':
    run(sys.argv[1], sys.argv[2], sys.argv[3])
