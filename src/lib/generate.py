"""Generate the blueprints from the page definitions.

  generate.py OUTDIR     write one blueprint per layout of every page in pages/ into OUTDIR

A blueprint = its page definition (pages/<page>.yaml) + the layout for its screen (specs/<spec>.py, what the drawing
reads) + the shared parts (pages/_shared.yaml, lib/shared.py). The macro files (custom_templates) are built separately
by lib/build_lib.py. After writing, lib/inputs_std.py puts the inputs in the input scheme's order.
"""
import glob, os, sys
LIB = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(LIB)
sys.path.insert(0, LIB); sys.path.insert(0, ROOT); sys.path.insert(0, os.path.join(ROOT, 'specs'))
import pageyaml as PY
import needs, inputs_std, shared
from build_lib import load_spec, LAYOUT_NAMES

import pages
SH = pages.shared()
KIT_READS = needs.fv(open(os.path.join(ROOT, 'ds_macros.jinja'), encoding='utf-8').read())
I = lambda n: PY.Input({'!input': n})

SHARED_BIND = [('font_dir', 'font_dir'), ('ds_devs', 'displays'), ('stale_after', 'stale_after'),
               ('weekday_lang', 'weekday_format'), ('time_format', 'time_format'), ('header_title', 'header_title')]


def merged(page, scr):
    """the page with one layout's differences applied"""
    lay = dict(page['layouts'][scr], screen=scr)
    from layouts import layouts             # the blueprint's name, file and source follow from the page and the screen
    d = next((l for l in layouts() if l['page'] == page['page'] and l['screen'] == str(scr)), None)
    if d:
        lay = dict({'name': d['title'], 'blueprint': d['blueprint'], 'source_url': d['source_url']}, **lay)
    p = dict(page)
    p['data'] = dict(page.get('data') or {})
    inputs = [i for i in page.get('inputs', []) if i['name'] not in (lay.get('drop_inputs') or [])]
    for i in lay.get('inputs') or []:
        k = [n for n, x in enumerate(inputs) if x['name'] == i['name']]
        i = {kk: vv for kk, vv in i.items() if kk != 'after'}
        if k:
            inputs[k[0]] = i
        else:
            after = (lay['inputs'][[x['name'] for x in lay['inputs']].index(i['name'])]).get('after')
            pos = [n for n, x in enumerate(inputs) if x['name'] == after]
            inputs.insert(pos[0] + 1 if pos else len(inputs), i)
    p['inputs'] = inputs
    vs = list(p['data'].get('variables') or [])
    for v in lay.get('variables') or []:
        n = list(v)[0]
        k = [j for j, x in enumerate(vs) if list(x)[0] == n]
        if k:
            vs[k[0]] = v
        else:
            vs.append(v)
    p['data']['variables'] = vs
    for k in ('steps', 'draw'):
        if k in lay:
            p['data'][k] = lay[k]
    return p, lay


# ---- inputs ---------------------------------------------------------------------------------------------------------

def shared_inputs(p, lay):
    names = ['displays']
    if p['redraw'] == 'button':
        names.append('button_entity')
    if p['redraw'] == 'trigger':
        names.append('automation_trigger')
    names += ['automation_conditions', 'header_title', 'time_format', 'weekday_format', 'rotate']
    if p.get('stale'):
        names.append('stale_after')
    if p['redraw'] in ('trigger', 'button'):
        names += ['led_color', 'led_flash_delay']
    names.append('font_dir')
    out = []
    for n in names:
        d = dict(SH['inputs'][n + ('@' + p['redraw'] if n + '@' + p['redraw'] in SH['inputs'] else '')])
        dflt = {**(p.get('defaults') or {}), **(lay.get('defaults') or {})}
        if n in dflt:
            d['default'] = dflt[n]
        h = help_text(n, p, lay, d)
        if h:
            d['description'] = h
        out.append((n, d))
    return out


def help_text(n, p, lay, d):
    """the shared inputs' help, made specific to the page and the screen"""
    scr = lay['screen']
    f = SH['screen_facts'][scr]
    desc = p.get('description') or {}
    if n == 'displays' and p['redraw'] != 'button':
        return f"The {f['size']} devices to draw on"
    if n == 'rotate':
        up = int(d.get('default', 0))
        if scr == '14':
            return f"Display rotation in degrees. {f['native']}: {up} draws this layout upright."
        return f"Display rotation in degrees. {f['native']}: {up} draws this layout upright, {(up + 180) % 360} upside down."
    if n == 'header_title':
        t = lay.get('title_default') or desc.get('title_default')
        if not t:
            en = ((p.get('texts') or {}).get('en') or {})
            t = '"' + (en.get('default_title') or en.get('title')) + '"' if (en.get('default_title') or en.get('title')) else "the page's name"
        return f"Shown in capitals at the top left. Leave blank for {t} in your language."
    if n == 'time_format':
        return f"12-hour (AM/PM) or 24-hour clock for {desc.get('times', 'the times on the display')}."
    return None


def input_block(p, lay):
    blocks = []
    for n, d in shared_inputs(p, lay):
        blocks.append((n, d, inputs_std.section_of(n)))
    for i in p['inputs']:
        d = {}
        for k, kk in (('label', 'name'), ('help', 'description')):
            if k in i:
                d[kk] = i[k]
        if 'default' in i and not i.get('required'):
            d['default'] = i['default']
        d['selector'] = i['selector']
        blocks.append((i['name'], d, i.get('section') or 'content'))
    out = {}
    for key, title, icon, collapsed, _ in inputs_std.SECTIONS:
        mine = {n: d for n, d, s in blocks if s == key}
        if mine:
            sec = {'name': title, 'icon': icon}
            if collapsed:
                sec['collapsed'] = True
            sec['input'] = mine
            out[key] = sec
    return out


# ---- variables ------------------------------------------------------------------------------------------------------

def binds(p):
    """input -> variable names, for the page's own inputs and extra bindings of shared inputs"""
    b = {}
    for x in p.get('bind') or []:
        if isinstance(x, str):
            b.setdefault(x, []).append(x)
        else:
            for i, v in x.items():
                b.setdefault(i, []).extend(v if isinstance(v, list) else [v])
    return b


def stale_vars(entities):
    lst = ', '.join(entities)
    return {'ds_last_ts': ('{% set ns = namespace(t=0) %} {% for e in [' + lst + '] %}\n'
                           '  {% if e %}{% for s in expand(e) %}{% set ns.t = [ns.t, as_timestamp(s.last_reported | default(s.last_updated), 0)] | max %}{% endfor %}{% endif %}\n'
                           '{% endfor %} {{ ns.t }}'),
            'ds_stale': shared.STALE}


def variables(p, lay):
    v = {'ds_set': SET_ID}            # the set id (lib/set_id.py fills it in): the templates compare it with theirs
    b = binds(p)
    if p.get('ds_in'):
        din = {}
        for var, inp in SHARED_BIND:
            if inp == 'stale_after' and not p.get('stale'):
                continue
            din[var] = I(inp)
        bound = {i for i in b}
        for i in p['inputs']:
            if i['name'] not in bound:
                din[i['name']] = I(i['name'])
        v['ds_in'] = din
        for i, vs in b.items():
            for x in vs:
                v[x] = I(i)
    else:
        for var, inp in SHARED_BIND:
            if inp == 'stale_after' and not p.get('stale'):
                continue
            v[var] = I(inp)
        for i, vs in b.items():
            for x in vs:
                v[x] = I(i)
    if p.get('texts'):                     # a page's own texts, whether it passes its inputs as ds_in or one by one
        v['language_map'] = PY.load(shared.TEXTS['language_map'].replace('PAGE', p['page']))
        if 'weekdays' in (p['texts'].get('use') or {}):
            v['weekday_short_map'] = PY.load(shared.TEXTS['weekday_short_map'])
            v['months_short_map'] = PY.load(shared.TEXTS['months_short_map'])
    for k, x in (lay.get('constants') or {}).items():
        v[k] = x
    for c in p['data'].get('variables') or []:
        v.update(c)
    if isinstance(p.get('stale'), list):
        v.update(stale_vars(p['stale']))
    return v


# ---- actions --------------------------------------------------------------------------------------------------------

def draw_args(spec, view, varnames):
    body = spec.PAYLOADS[['main', 'error'].index(view)]
    want = sorted(n for n in (needs.fv(body) | KIT_READS) - needs.PROVIDED if n in varnames and n not in ('ds_devs', 'font_dir'))
    return ['ds_devs', 'font_dir'] + want


def weather_extras(spec, names):
    """a weather layout's own data beyond the weather model: the page's variables its drawing reads (a module beside the
    weather, e.g. the calendar), handed over with the weather call; none for a weather-only page"""
    reads = set()
    for body in spec.PAYLOADS:
        reads |= needs.fv(body)
    return sorted(n for n in reads - needs.PROVIDED - KIT_READS if n in names and n not in ('ds_devs', 'font_dir', 'ds_in'))


def draw_step(payload):
    return {'action': 'opendisplay.drawcustom', 'target': {'device_id': I('displays')},
            'data': {'background': 'white', 'dither': 'none', 'rotate': I('rotate'), 'payload': payload}}


SET_ID = '@@EPSET@@'


def payload(layout, view, args):
    d = ', '.join(f"'{n}': {n}" for n in ['ds_set'] + [a for a in args if a != 'ds_set'])
    return ("{%- from 'ep_design.jinja' import ep_draw -%} {{- (ep_draw | as_function)('" + layout + "', '" + view +
            "', {" + d + "}) -}}")


def step_vars(steps):
    out = set()
    for s in steps or []:
        if 'variables' in s:
            out |= set(s['variables'])
        if 'response_variable' in s:
            out.add(s['response_variable'])
        for k in ('then', 'else', 'sequence', 'default'):
            if isinstance(s.get(k), list):
                out |= step_vars(s[k])
    return out


def actions(p, lay, varnames):
    spec = load_spec(lay['spec'])
    layout = LAYOUT_NAMES[lay['spec']]
    data = p['data']
    acts = []
    if p['redraw'] == 'trigger':
        acts.append(SH['button_flash'])
    acts += data.get('steps') or []
    dr = data['draw']
    names = set(varnames) | step_vars(data.get('steps')) | step_vars(dr.get('steps'))
    if dr['kind'] == 'weather':
        pl, ex = SH['weather_payload'].replace('LAYOUT', layout), weather_extras(spec, names)
        if ex:
            a = 'ds_fh=ds_fh | default({}))'
            assert a in pl
            pl = pl.replace(a, 'ds_fh=ds_fh | default({}), ' + ', '.join(f'{n}={n}' for n in ex) + ')')
        acts.append(draw_step(pl))
    elif dr['kind'] == 'single':
        acts.append(draw_step(payload(layout, 'main', draw_args(spec, 'main', names))))
    else:
        acts.append({'choose': [{'conditions': dr['when'],
                                 'sequence': (dr.get('steps') or []) + [draw_step(payload(layout, 'main', draw_args(spec, 'main', names)))]}],
                     'default': [draw_step(payload(layout, 'error', draw_args(spec, 'error', set(varnames) | step_vars(data.get('steps')))))]})
    return acts


# ---- description ----------------------------------------------------------------------------------------------------

def description(p, lay, scr):
    d = p.get('description') or {}
    if not d:
        return lay.get('old_description', '')
    L = SH['links']
    integ = SH['integrations']
    out = [f"# {lay['name']}", '', d['shows'].strip()]
    if lay.get('shows'):
        out[-1] += ' ' + lay['shows'].strip()
    out += ['', '## Works with', '', SH['screens'][scr]]
    out += ['', '## Needs', '']
    needs_ = ['opendisplay'] + [n for n in (d.get('needs') or []) if n != 'opendisplay']
    for n in needs_:
        i = integ[n]
        line = f"- [{i['name']}]({i['url']})" + (f" ({i['min_version']} or later)" if i.get('min_version') else '')
        if i.get('what'):
            line += f": {i['what']}"
        out.append(line)
    for x in d.get('needs_also') or []:
        out.append(f'- {x}')
    out.append(shared.NOTE)
    out.append(f"- The design-system fonts in `/config/www/fonts/` (or another drawcustom font folder): {SH['fonts']}")
    for x in d.get('optional') or []:
        i = integ[x]
        out.append(f"- Optional: [{i['name']}]({i['url']}): {i['what']}")
    out += ['', '## Trigger advice', '', d['trigger_advice'].strip()]
    if p['redraw'] == 'trigger':
        out += ['', SH['button_advice'].strip()]
    notes = list(d.get('notes') or []) + list(lay.get('notes') or [])
    if notes:
        out += ['', '## Notes', ''] + [f'- {n.strip()}' for n in notes]
    out += ['', '## Links', '']
    for k in ('repository', 'design_system', 'trmnl_fonts', 'space_grotesk'):
        if L[k].get('url'):                      # a link without a URL yet (the repository) is left out
            out.append(f"- [{L[k]['name']}]({L[k]['url']})")
    for n in needs_ + list(d.get('optional') or []):
        out.append(f"- [{integ[n]['name']}]({integ[n]['url']})")
    for b in lay.get('based_on', d.get('based_on')) or []:
        out.append(f"- Inspired by: [{b['name']}]({b['url']})")
    out.append(f"- Made by [{L['author']['name']}]({L['author']['url']}), with Claude")
    return '\n'.join(out) + '\n'


# ---- one blueprint --------------------------------------------------------------------------------------------------

def blueprint(page, scr):
    p, lay = merged(page, scr)
    bp = {'name': lay['name'], 'description': description(p, lay, scr)}
    if lay.get('source_url'):
        bp['source_url'] = lay['source_url']
    bp['domain'] = 'automation'
    bp['input'] = input_block(p, lay)
    doc = {'blueprint': bp}
    data = p['data']
    if data.get('trigger_variables'):
        doc['trigger_variables'] = data['trigger_variables']
    v = variables(p, lay)
    if p['redraw'] == 'trigger':
        doc['variables'] = v
        doc['trigger'] = I('automation_trigger')
        doc['conditions'] = I('automation_conditions')
    else:
        doc['trigger'] = data['triggers']
        doc['conditions'] = I('automation_conditions')
        doc['variables'] = v
    doc['action'] = actions(p, lay, list(v))
    doc.update(data.get('mode') or {'mode': 'single', 'max_exceeded': 'silent'})
    return lay['blueprint'], doc


def main(outdir):
    os.makedirs(outdir, exist_ok=True)
    n = 0
    for pname in pages.names():
        page = pages.load(pname)
        for scr in page['layouts']:
            name, doc = blueprint(page, scr)
            open(os.path.join(outdir, name), 'w', encoding='utf-8').write(
                '# Generated by lib/generate.py from pages/' + pname + '.yaml: edit the page definition, not this file.\n'
                + PY.dump(doc))
            n += 1
    print(f'{n} blueprints written to {outdir}')


if __name__ == '__main__':
    main(sys.argv[1])
