#!/usr/bin/env python3
"""Build the shared design-system macro files (config/custom_templates) and the blueprints.

The macro files are generated from these sources:
  ds_macros.jinja        -> the drawing kit, nested inside ep_draw()
  specs/_wx.py WXM       -> the weather kit (weather layouts only)
  wx_steps.yaml (wx)     -> the weather data model
  wx_txt.yaml            -> weather texts (ep_i18n.jinja)
  specs/<layout>.py      -> each layout's main / error drawing code

usage: build_lib.py OUTDIR layout_key[,layout_key...]
  layout_key = spec module name, e.g. weather_35 (lib/layouts.py prints them all)
"""
import importlib.util, pathlib, re, sys, textwrap
import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
LIB = ROOT / 'lib'
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / 'specs'))
import json  # noqa: E402
import harness  # noqa: E402

# constants hoisted out of the kit into ep_metrics.jinja (built once per HA start, not per render)
HOIST = ['ADV', 'KRN', 'LSB', 'CAPUP', 'CAPDN', 'SGB', 'SGR', 'HUP', 'HDN', 'HWR', 'ICH', 'ICB', 'MDI']

# spec (the layout's drawing file) -> public layout name used by the blueprints: from the page definitions (lib/layouts.py)
sys.path.insert(0, str(LIB))
from layouts import layouts  # noqa: E402
LAYOUTS = layouts
LAYOUT_NAMES = {l['spec']: l['name'] for l in layouts()}


def layout_tiers():
    """layout key -> tier in ep_tokens.jinja (EP_TIER): the screen a page definition puts the layout on (pages/*.yaml
    layouts) and that screen's tier (derive_tokens.SCREEN_OF, next to the panel facts)"""
    sys.path.insert(0, str(LIB))
    import pages
    from derive_tokens import SCREEN_OF
    tier_of = {scr: t for t, scr in SCREEN_OF.items()}
    out = {}
    for name in pages.names():
        for scr, lay in (pages.load(name).get('layouts') or {}).items():
            spec, tier = lay['spec'], tier_of[str(scr)]
            if out.setdefault(spec, tier) != tier:
                sys.exit(f'{spec}: on two tiers ({out[spec]}, {tier}) in the page definitions')
    return out


TIERS = layout_tiers()


def tokenise(body, key, name):
    """Layouts read their canvas and frame from the tier tokens (EP_TK); a literal frame would let the token table and
    the layouts drift apart, so the build refuses one."""
    assert not re.search(r'\{%- set W, H, P, TH = \d', body), f'{name}: literal frame, use EP_TK'
    return body


def load_spec(key):
    p = ROOT / 'specs' / f'{key}.py'
    s = importlib.util.spec_from_file_location(key, p)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


def split_kit():
    kit, metrics = [], []
    for line in (ROOT / 'ds_macros.jinja').read_text(encoding='utf-8').split('\n'):
        m = re.match(r'^\{%- set (\w+) = ', line)
        if m and m.group(1) in HOIST:
            metrics.append(line)
        else:
            kit.append(line)
    return '\n'.join(kit).strip('\n'), '\n'.join(metrics)


def wtxt_dict():
    src = (ROOT / 'wx_txt.yaml').read_text(encoding='utf-8')
    m = re.search(r'\{% set m = (\{.*\}) %\}', src, re.S)
    return textwrap.dedent(m.group(1))


def wx_model():
    """The weather data model template, turned from 'output a dict' into 'set wx = dict'."""
    steps = yaml.safe_load((ROOT / 'wx_steps.yaml').read_text(encoding='utf-8'))
    tmpl = [s for s in steps if 'variables' in s and 'wx' in s['variables']][0]['variables']['wx']
    i = tmpl.rfind('{{ {')
    j = tmpl.rfind('} }}')
    assert i > 0 and j > i
    return tmpl[:i] + '{%- set wx = {' + tmpl[i + 4:j] + '} -%}' + tmpl[j + 4:]


def ink_template():
    """ds_ink (the panels' colour capability), from ink.jinja without its header comment."""
    return re.sub(r'^\{#-.*?-#\}\n', '', (ROOT / 'ink.jinja').read_text(encoding='utf-8'), flags=re.S)


def input_names():
    """Every input the drawing can be handed, across the blueprints: each blueprint's own variables (outside its actions) that are a plain
    !input and the keys of its ds_in (the inputs dict ep_draw receives), as the generator writes them (lib/generate.py)."""
    import generate, pageyaml, pages
    names = set()
    for name in pages.names():
        page = pages.load(name)
        for scr in page['layouts']:
            for k, v in generate.variables(*generate.merged(page, scr)).items():
                if k == 'ds_in':
                    names |= set(v)
                elif isinstance(v, pageyaml.Input):
                    names.add(k)
    return sorted(names)


PASSED = {}  # layout -> computed blueprint variables its drawing reads


def layout_passed():
    """layout -> the computed variables (not inputs) its blueprint hands the drawing: what the generator passes to ep_draw
    (lib/generate.py draw_args: what the layout's payloads and the kit read, among the blueprint's variables), less the
    inputs. Weather layouts get theirs from the weather data model instead."""
    import generate, pages
    inputs = set(input_names()) | {'ds_devs', 'font_dir'}
    out = {}
    for name in pages.names():
        page = pages.load(name)
        for scr, lay0 in page['layouts'].items():
            p, lay = generate.merged(page, scr)
            data = p['data']
            sp = load_spec(lay0['spec'])
            names = set(generate.variables(p, lay)) | generate.step_vars(data.get('steps')) | generate.step_vars(data['draw'].get('steps'))
            if data['draw']['kind'] == 'weather':      # the weather model plus what else the page hands over (generate.weather_extras)
                out[LAYOUT_NAMES[lay0['spec']]] = generate.weather_extras(sp, names)
                continue
            args = set()
            for view in ['main', 'error'][:len(sp.PAYLOADS)]:
                args |= set(generate.draw_args(sp, view, names))
            out[LAYOUT_NAMES[lay0['spec']]] = sorted(args - inputs)
    return out


def build_design(keys):
    kit, _ = split_kit()
    passed = layout_passed()
    from _wx import WXM
    layouts, bodies, wxm_needed = {}, [], False
    for key in keys:
        sp = load_spec(key)
        name = LAYOUT_NAMES[key]
        fam = 'weather' if getattr(sp, 'WX', False) else 'other'
        layouts[name] = {'kit': fam, 'tier': TIERS[key],
                         'page': next(l['page'] for l in LAYOUTS() if l['spec'] == key)}
        views = ['main', 'error'][:len(sp.PAYLOADS)]
        extra = ''      # a weather layout reads the weather data model and the weather words (ds_wtxt), plus what its page adds
        if fam != 'weather' or passed.get(name):
            # the blueprint keeps its own data and texts and passes what the drawing reads
            own = passed[name]
            PASSED[name] = own
            extra = '\n'.join(f'{{%- set {n} = c.{n} -%}}' for n in own)
        for view, body in zip(views, sp.PAYLOADS):
            if body.startswith(WXM):
                body = body[len(WXM):]
                wxm_needed = True
            bodies.append((name, view, ((extra + '\n') if extra else '') + tokenise(body.strip('\n'), key, name)))
    names = [n for n in input_names() if n not in ('ds_devs',)]
    out = []
    out.append('''{#- ===========================================================================
    E-paper design system: DRAWING
    ---------------------------------------------------------------------------
    One entry point for every blueprint:

      {%- from 'ep_design.jinja' import ep_draw -%}
      {{- (ep_draw | as_function)(layout, view, inputs) -}}

    layout  a layout name, e.g. 'weather_35' (see EP_LAYOUTS below)
    view    'main', or 'error' when the blueprint has no data to show
    inputs  a dict of the blueprint's inputs (the blueprint's ds_in variable)
            plus what its actions fetched (forecasts, events)
    returns the drawcustom payload: a list of elements

    Sections, top to bottom:
      1. inputs          the blueprint's inputs, by their variable names
      2. tokens          ep_tokens.jinja resolved for this layout's tier and these panels
      3. data models     shared per kit (weather: wx)
      4. kit             text measuring and drawing primitives (T, R, L, I, chips,
                         title row, rows, glance hero, ...), shared by every layout
      5. kits     shared per kit (weather: cells, chips, PICK)
      6. layouts         one block per layout and view

    Generated by lib/build_lib.py from the sources; edit the sources, not this file.
    Reload after replacing it: homeassistant.reload_custom_templates
    =========================================================================== -#}
{%- from 'ep_tokens.jinja' import EP_TIER, EP_LAYOUT, EP_FONT, EP_COLOR, EP_SPACE, EP_STROKE, EP_ICON, EP_CHART -%}
{%- from 'ep_metrics.jinja' import ''' + ', '.join(HOIST) + ''' -%}
{%- from 'ep_i18n.jinja' import EP_WTXT, EP_DAYS_SHORT, EP_MONTHS_SHORT, EP_TXT, EP_SETTXT -%}
{#- the set id: a hash of the four templates, written by lib/set_id.py; every blueprint of the same release carries it -#}
{%- set EP_SET = '@@EPSET@@' -%}
''')
    out.append('{%- set EP_LAYOUTS = {\n' + ',\n'.join(
        f"  '{n}': {{'kit': '{d['kit']}', 'tier': '{d['tier']}', 'page': '{d['page']}'" + "}" for n, d in layouts.items()) + '\n} -%}\n')
    out.append('{%- macro ep_draw(layout, view, c, returns) -%}\n')
    # a layout name these templates don't know is a blueprint from another release: the update screen, on the smallest canvas
    small = min((l for l in LAYOUTS() if l['name'] in layouts), key=lambda l: l['canvas'][0] * l['canvas'][1])['name']
    out.append(f"{{%- set EP_L = EP_LAYOUTS[layout] if layout in EP_LAYOUTS else EP_LAYOUTS['{small}'] -%}}\n")
    out.append('{#- ---- 1. inputs: the blueprint variable names.\n'
               '     A missing input is undefined ---- -#}\n')
    for n in names:
        out.append(f'{{%- set {n} = c.{n} -%}}\n')
    out.append('{%- set ds_devs = c.ds_devs -%}\n')
    out.append('{%- set forecast_entity = c.forecast_entity -%}\n')
    out.append('{%- set ds_fd = c.ds_fd -%}\n{%- set ds_fh = c.ds_fh -%}\n')
    out.append('''{#- ---- 2. tokens, resolved ---- -#}
{%- set font_dir = font_dir if font_dir is string else '' -%}
{#- a layout that serves several panel heights (the rain chart: 3.5" or 2.7") takes the tier of the panel's canvas -#}
{%- set EP_TT, EP_LT = EP_TIER[EP_L.tier], (EP_LAYOUT[layout] | default({})) -%}
{#- the layout's measured tokens (its hero, its strip icons) laid over its tier's -#}
{%- set EP_TK = dict(EP_TT, type=dict(EP_TT.type, **(EP_LT.type | default({}))), icon=dict(EP_TT.icon, **(EP_LT.icon | default({})))) -%}
{#- an item's main text line: type.primary, or type.data where a screen has none (*Deriving tokens for any screen*, the size classes); [Regular, Bold] -#}
{%- set EP_PRIMARY = EP_TK.type.primary if EP_TK.type.primary else [EP_TK.type.data, EP_TK.type.data] -%}
{#- the kit's short names for the font roles (TRMNL12/16 text is always the bold cut) -#}
{%- set f12 = font_dir ~ EP_FONT.label12 -%}
{%- set f12b = f12 -%}
{%- set f16 = font_dir ~ EP_FONT.label16 -%}
{%- set f16b = f16 -%}
{%- set f12r = font_dir ~ EP_FONT.unit12 -%}
{%- set f16r = font_dir ~ EP_FONT.unit16 -%}
{%- set f21 = font_dir ~ EP_FONT.text21 -%}
{%- set f21b = font_dir ~ EP_FONT.strong21 -%}
{%- set fhero = font_dir ~ EP_FONT.hero -%}
{%- set font_file = f16 -%}
{#- panel capability: 'r' red, 'y' yellow, 'g' grayscale, for every device selected in displays -#}
{%- set ds_ink -%}''' + ink_template().strip() + '''{%- endset -%}
{%- set ds_ink = ds_ink | trim -%}
{%- set SEV = EP_COLOR.severe.red if 'r' in ds_ink else (EP_COLOR.severe.yellow if 'y' in ds_ink else (EP_COLOR.severe.gray if 'g' in ds_ink else EP_COLOR.severe.mono)) -%}
{%- set WARN = EP_COLOR.warning.red_yellow if ('r' in ds_ink and 'y' in ds_ink) else (EP_COLOR.warning.gray if 'g' in ds_ink else EP_COLOR.warning.mono) -%}
{#- the colour tokens for the selected panels (design system: Colour tokens, Values per panel); color.warningChip is chip.warning's fill, or 'outline' -#}
{%- set color = {'ink': EP_COLOR.ink, 'paper': EP_COLOR.paper, 'severe': SEV.severe, 'onSevere': SEV.onSevere, 'severeMark': SEV.severeMark, 'warning': WARN.warning, 'onWarning': WARN.onWarning, 'warningChip': WARN.chip} -%}
''')
    out.append('{#- ---- 3. data models ---- -#}\n')
    out.append("{%- if EP_L.kit == 'weather' -%}\n{%- set ds_wtxt = EP_WTXT[weekday_lang] -%}\n"
               "{%- if view == 'main' -%}\n" + wx_model().strip('\n') + "\n{%- endif -%}\n{%- endif -%}\n")
    out.append('{#- ---- 4. kit ---- -#}\n' + kit + '\n')
    if wxm_needed:
        out.append("{#- ---- 5. weather kit (also used by the doors & windows glance) ---- -#}\n" + WXM.strip('\n') + '\n')
    out.append('{#- ---- 6. layouts ---- -#}\n')
    out.append("""{#- one set (design system: Blueprint mechanics, One set): a blueprint whose set id differs from these templates' draws
     the title row and the error block only: the message and, on new lines under it, the two ids (one line where that
     fits, else one each; a blueprint without an id shows the missing value). Compared as text: Home Assistant may hand a
     value over as a number. The lines are wrapped here and drawn one by
     one, so the ids always start a line; the block of lines is centred in the fill -#}
{%- if layout not in EP_LAYOUTS or (c.ds_set | default('—') | string) != (EP_SET | string) -%}
{%- set W, H, P, TH = EP_TK.width, EP_TK.height, EP_TK.space.pad, EP_TK.space.titleRow -%}
{%- set pt = (EP_TXT[EP_L.page] | default({}))[weekday_lang] | default({}) -%}
{{- TITLE(ns, header_title if header_title else (pt.default_title | default(EP_WTXT[weekday_lang].title)), as_timestamp(now()), W, P, TH) -}}
{%- set tt = EP_TK.type.title -%}{%- set sx = SPACE_S(tt[1]) | int -%}{%- set mw = W - 2 * P - 2 * sx -%}
{%- set y0, y1 = P + TH + (P // 2), H - P -%}
{{- R(ns, P - sx, y0, W - P - 1 + sx, y1 - 1, color.severe) -}}
{%- set w = namespace(lines=[], cur='') -%}
{%- for word in (EP_SETTXT[weekday_lang] | upper).split(' ') -%}
{%- set t = (w.cur ~ ' ' ~ word) if w.cur else word -%}
{%- if w.cur and (VALUE_W(t, tt[1], FONT[tt[0]]) | int) > mw -%}{%- set w.lines = w.lines + [w.cur] -%}{%- set w.cur = word -%}{%- else -%}{%- set w.cur = t -%}{%- endif -%}
{%- endfor -%}
{%- set a, b = 'BLUEPRINT ' ~ (c.ds_set | default('—') | upper), 'TEMPLATES ' ~ (EP_SET | upper) -%}
{%- set lines = w.lines + [w.cur] + ([a ~ ' · ' ~ b] if (VALUE_W(a ~ ' · ' ~ b, tt[1], FONT[tt[0]]) | int) <= mw else [a, b]) -%}
{%- set pitch = tt[1] + sx -%}
{%- set yc = (y0 + y1) // 2 - ((lines | length) - 1) * pitch // 2 -%}
{%- for s in lines -%}
{%- set ns.el = ns.el + [{'type': 'text', 'value': s, 'x': W // 2, 'y': yc + loop.index0 * pitch, 'font': FONT[tt[0]], 'size': tt[1], 'color': color.onSevere, 'anchor': 'mm'}] -%}
{%- endfor -%}
""")
    first = False
    for name, view, body in bodies:
        kw = 'if' if first else 'elif'
        first = False
        out.append(f"{{%- {kw} layout == '{name}' and view == '{view}' -%}}\n" + body + '\n')
    out.append('{%- endif -%}\n')
    out.append('{{- OMERGE(ns) -}}\n{%- do returns(ns.el) -%}\n{%- endmacro -%}\n')
    return ''.join(out)


def build_metrics():
    _, metrics = split_kit()
    return ('''{#- ===========================================================================
    E-paper design system: FONT AND ICON METRICS (generated data)
    ADV  glyph advances of the TRMNL cuts (bold and regular 12/16/21), for measuring text
    KRN  kerning between capitals, digits and number punctuation (the renderer applies it)
    LSB  left side bearings per font ('_' = every other glyph)
    CAPUP / CAPDN  cap-height ink above / below the middle anchor per size
    SGB  Space Grotesk Bold hero numerals: ink offset of the first digit
    MDI  Material Design Icons code points, drawn as text so icons stay pixel-exact
    Change only together with the fonts. Built once per Home Assistant start.
    =========================================================================== -#}
''' + metrics + '\n')


def check_texts(com, pages):
    """every text is a string (YAML reads an unquoted On, No or Yes as a boolean), and the short names follow
    *Text rules*, *Eight languages*: a weekday is 2 letters and a month 3, in every language"""
    errs = []
    def leaves(x, path):
        if isinstance(x, dict):
            for k, v in x.items():
                leaves(v, path + [str(k)])
        elif isinstance(x, list):
            for i, v in enumerate(x):
                leaves(v, path + [str(i)])
        elif not isinstance(x, str):
            errs.append(f"{'/'.join(path)} is {x!r}, not a text (quote it)")
    leaves(com, ['_shared'])
    leaves(pages, [])
    for key, n, count in (('weekdays_short', 2, 7), ('months_short', 3, 12)):
        for lang, names in com[key].items():
            bad = [v for v in names if not isinstance(v, str) or len(v) != n]
            if bad or len(names) != count:
                errs.append(f'{key} {lang}: {count} names of {n} letters each (*Text rules*, *Eight languages*), not {names}')
    if errs:
        sys.exit('texts:\n  ' + '\n  '.join(errs))


def page_texts():
    """EP_TXT (page -> language -> texts, with the shared day and month lists it uses), EP_DAYS_SHORT and EP_MONTHS_SHORT,
    from the page definitions (pages/<page>.yaml, `texts`; the shared day and month lists in pages/_shared.yaml): every page's texts in one place instead of a copy in each blueprint."""
    import pages
    com = pages.shared()['texts']
    t = {'pages': {}}
    for name in pages.names():
        p = pages.load(name)
        if p.get('texts'):
            t['pages'][p['page']] = p['texts']
    check_texts(com, t['pages'])
    J = lambda v: json.dumps(v, ensure_ascii=False)
    pages = []
    for p, pg in t['pages'].items():
        use = pg.get('use') or {}
        langs = [l for l in pg if l != 'use']
        per = {l: dict(pg[l], **{k: com[c][l] for k, c in use.items()}) for l in langs}
        pages.append(f"  '{p}': {J(per)}")
    return ("{#- EP_TXT  per-page texts (titles, messages, labels), from the page definitions -#}\n"
            "{%- set EP_TXT = {\n" + ',\n'.join(pages) + "\n} -%}\n"
            "{%- set EP_DAYS_SHORT = " + J(com['weekdays_short']) + " -%}\n"
            "{%- set EP_MONTHS_SHORT = " + J(com['months_short']) + " -%}\n"
            "{#- EP_SETTXT  the message when a blueprint and the templates are from different releases -#}\n"
            "{%- set EP_SETTXT = " + J(com['set_mismatch']) + " -%}\n")


def build_i18n():
    return ('''{#- ===========================================================================
    E-paper design system: TEXTS
    EP_WTXT  weather words per language (labels, condition names, warning codes)
    =========================================================================== -#}
{%- set EP_WTXT = ''' + wtxt_dict().strip() + ''' -%}
''' + page_texts())


if __name__ == '__main__':
    outdir = pathlib.Path(sys.argv[1])
    keys = sys.argv[2].split(',')
    ct = outdir / 'custom_templates'
    ct.mkdir(parents=True, exist_ok=True)
    (ct / 'ep_tokens.jinja').write_text((LIB / 'ep_tokens.jinja').read_text(encoding='utf-8'), encoding='utf-8')
    (ct / 'ep_metrics.jinja').write_text(build_metrics(), encoding='utf-8')
    design = build_design(keys)
    (ct / 'ep_i18n.jinja').write_text(build_i18n(), encoding='utf-8')
    (ct / 'ep_design.jinja').write_text(design, encoding='utf-8')
    for f in sorted(ct.glob('*.jinja')):
        print(f'{f.name}: {f.stat().st_size} bytes')
