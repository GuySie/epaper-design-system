"""The design system's per-tier token tables (type, space, icons), generated from ep_tokens.jinja so the document can't
drift from the code. Used by registry.py (blocks tier-type, tier-space, tier-icon). Notes in brackets come from NOTES."""
import json, pathlib, sys
import jinja2

LIB = pathlib.Path(__file__).parent
sys.path.insert(0, str(LIB))
from derive_tokens import KNOWN, SCREEN_OF, ALSO, TRMNL, X_DATA_MM, X_LABEL_MM, X_CAPS_ONLY_MM, STROKE_MIN_MM, NATIVE_TOL_MM, PAD_SHARE, PAD_MIN_MM, HERO_GAP_DIV   # noqa: E402

SRC = LIB / 'ep_tokens.jinja'
from layouts import registry          # noqa: E402
REG = registry()
TIERS = sorted(KNOWN, key=lambda t: REG['screens'].index(SCREEN_OF[t]))   # the tiers (panel facts: derive_tokens), in the registry's screen order
SCREEN = {t: REG['screen_names'][SCREEN_OF[t]] for t in TIERS}      # screen names: registry.yaml


def notes(T):
    """(token, tier) -> note after the value, from the rules: a label cut the floor allows in capitals only, and the
    pages that draw a hero on its own on the tier (the Glance pages with a blueprint there)"""
    n = {}
    for t in TIERS:
        lab = T[t]['type']['label']
        if lab[1] == 12 and TRMNL[12]['x'] * T[t]['pitch'] < X_CAPS_ONLY_MM:      # the floor allows TRMNL12 under 1.1 mm in capitals only
            n[('type.label', t)] = 'caps only'
    return n


NOTES = {}
TYPE_ROWS = [('title', ''), ('stamp', ''), ('label', ' (field labels, captions)'), ('fieldLabel', ' (labels beside a hero)'),
             ('data', ' (values, names, cells)'), ('primary', " (an item's main line)"), ('secondary', ' (the Glance secondary under the hero)'),
             ('unit', ' (after `type.data`)')]
SPACE_ROWS = [('pad', ' (P)', f'~{PAD_SHARE * 100:g} % of the short side, ≥ {PAD_MIN_MM:g} mm, even'), ('m', ' (M)', '`space.pad` ÷ 2'), ('l', ' (L)', '`space.pad`'),
              ('titleRow', ' (TH)', 'cap height of `type.title` + `space.s` + `line.base`'),
              ('row', ' (list row)', '`rowMin` + 2 × `space.s`'),
              ('rowDense', ' (calendar, plant list)', '`rowMin` + `space.s` + `space.xs`'),
              ('detailRow', '', '`rowMin` + `space.xs`: label/value rows beside a hero'),
              ('footer', '', 'footer: `line.base` + `space.s` + cap height of `type.data`'),
              ('axis', '', 'chart axis under the baseline: `line.tick` + `space.s` + cap height of `type.label`')]
ICON_ROWS = ['min', 'inline']


def load():
    src = SRC.read_text()
    env = jinja2.Environment()
    return json.loads(env.from_string(src + '{{ EP_TIER | tojson }}').render())


def load_layouts():
    """EP_LAYOUT: each layout's measured tokens, by its public name"""
    return json.loads(jinja2.Environment().from_string(SRC.read_text() + '{{ EP_LAYOUT | tojson }}').render())


def font(v):
    if v is None:
        return '—'
    if isinstance(v[0], list):
        return ' / '.join(font(x) for x in v)
    name, size = v
    w = 'R' if name.startswith(('unit', 'text')) else 'B'
    return f'{size} {w}'


def cell(tok, tier, val):
    n = NOTES.get((tok, tier))
    return f'{val} {n}' if n else val


def header(extra=''):
    h = '| Token | ' + ' | '.join(f'{SCREEN[t]} `{t}`' for t in TIERS) + (' | Rule |' if extra else ' |')
    return [h, '|---|' + '---|' * len(TIERS) + ('---|' if extra else '')]


def tables():
    T = load()
    NOTES.update(notes(T))
    rows = header()
    for k, label in TYPE_ROWS:
        vals = []
        for t in TIERS:
            v = T[t]['type'].get(k)
            v = (str(v) if v is not None else '—') if k.startswith('hero') else font(v)
            vals.append(cell(f'type.{k}', t, v))
        rows.append(f'| `type.{k}`{label} | ' + ' | '.join(vals) + ' |')
    out = {'tier-type': rows}
    rows = header('rule')
    for k, label, rule in SPACE_ROWS:
        vals = [str(T[t]['space'].get(k)) if T[t]['space'].get(k) is not None else '—' for t in TIERS]
        rows.append(f'| `space.{k}`{label} | ' + ' | '.join(vals) + f' | {rule} |')
    rows.append(f'| `space.heroGap` | hero ÷ {HERO_GAP_DIV} |' + ' |' * (len(TIERS) - 1) + ' number ↔ icon, hero ↔ secondary, hero clearance |')
    out['tier-space'] = rows
    rows = header()
    for k in ICON_ROWS:
        vals = []
        for t in TIERS:
            v = T[t]['icon'].get(k)
            if v is None:
                s = '—'
            elif isinstance(v, list):
                s = f'{v[0]} → {v[-1]}'
            else:
                s = str(v)
            vals.append(cell(f'icon.{k}', t, s))
        rows.append(f'| `icon.{k}` | ' + ' | '.join(vals) + ' |')
    out['tier-icon'] = rows
    out.update(physical(T))
    return {k: '\n'.join(v) for k, v in out.items()}


# ---- what a layout budgets with, and what the sizes measure in millimetres: computed from the tokens, never typed ----
import re                                                                               # noqa: E402
ADV_AVG = {12: 7.7, 16: 9.3, 21: 13.5}     # the TRMNL Bold cuts' average advance (font metric): character budgets plan with it
# screens as people name them (a landscape and a portrait tier of one panel share a column)
GROUPS = []
for _t in TIERS:
    _g = SCREEN[_t].replace(' L', '').replace(' P', '')
    if GROUPS and GROUPS[-1][0] == _g:
        GROUPS[-1][1].append(_t)
    else:
        GROUPS.append((_g, [_t]))


def _macro_dict(name):
    src = (pathlib.Path(__file__).parent.parent / 'ds_macros.jinja').read_text()
    return eval(re.search(r'\{%%- set %s = (\{.*?\}) -%%\}' % name, src).group(1))


def physical(T):
    capdn, hup, hdn = _macro_dict('CAPDN'), _macro_dict('HUP'), _macro_dict('HDN')
    out = {}
    # panel budgets: rows as the lists fill them (KVFIT: the last row's ink ends above the bottom padding), characters per text line
    rows = ['| Screen | Canvas | Pixel pitch | Row h (dense) | Rows (dense) | Chars / text line | Chars / half column |', '|---|---|---|---|---|---|---|']
    for t in TIERS:
        e = T[t]; W, H = e['width'], e['height']; sp = e['space']; ds = e['type']['data'][1]
        P, top, yb = sp['pad'], sp['pad'] + sp['titleRow'] + sp['m'], H - sp['pad'] - 1
        fit = lambda rh: (yb - top - rh // 2 - capdn[ds]) // rh + 1
        dense = sp['rowDense'] != sp['row']
        rh = f"{sp['row']}" + (f" ({sp['rowDense']})" if dense else '')
        n = f"{fit(sp['row'])}" + (f" ({fit(sp['rowDense'])})" if dense else '')
        cw, half = (W - 2 * P) / ADV_AVG[ds], (W - 2 * P - sp['l']) / 2 / ADV_AVG[ds]
        rows.append(f"| {SCREEN[t]} | {W}×{H} | {e['pitch']} mm | {rh} | {n} | {int(cw)} | {int(half) if W > 200 else '—'} |")
    out['tier-budget'] = rows
    # padding in millimetres and as a share of the short side
    rows = ['| Screen | Padding | mm | % of short side |', '|---|---|---|---|']
    for t in TIERS:
        e = T[t]; P = e['space']['pad']
        rows.append(f"| {SCREEN[t]} | {P} px | {P * e['pitch']:.1f} | {100 * P / min(e['width'], e['height']):.1f} |")
    out['tier-pad'] = rows
    # each native cut's x-height / cap height per screen, and what the floors let it carry
    head = '| Font (x / cap px) | ' + ' | '.join(f"{g} ({T[ts[0]]['pitch']} mm)" for g, ts in GROUPS) + ' |'
    rows = [head, '|---|' + '---|' * len(GROUPS)]
    for size in (12, 16, 21):
        m = TRMNL[size]; cells = []
        for g, ts in GROUPS:
            pt = T[ts[0]]['pitch']; x, cap = m['x'] * pt, m['cap'] * pt
            role = ('data' if x >= X_DATA_MM else 'data (native tolerance)' if size == 21 and x >= X_DATA_MM - NATIVE_TOL_MM
                    else 'labels' if x >= X_CAPS_ONLY_MM or (size != 12 and x >= X_LABEL_MM) else 'labels in capitals' if x >= X_LABEL_MM else '✕')
            cells.append(f'{x:.2f} / {cap:.2f} mm {role}')
        rows.append(f"| TRMNL{size} ({m['x']} / {m['cap']}) | " + ' | '.join(cells) + ' |')
    out['tier-fonts'] = rows
    # stems: Regular and Bold per native cut, in millimetres; ✕ under stroke.min
    cuts = [('TRMNL12 / 16 Regular', 'r', 16), ('TRMNL12 / 16 Bold', 'b', 16), ('TRMNL21 Regular', 'r', 21), ('TRMNL21 Bold', 'b', 21)]
    rows = ['| | ' + ' | '.join(c[0] for c in cuts) + ' |', '|---|' + '---|' * len(cuts),
            '| Pixels | ' + ' | '.join(str(TRMNL[sz][k]) for _, k, sz in cuts) + ' |']
    for g, ts in GROUPS:
        pt = T[ts[0]]['pitch']
        rows.append(f'| {g} | ' + ' | '.join(f"{TRMNL[sz][k] * pt:.2f} mm" + (' ✕' if TRMNL[sz][k] * pt < STROKE_MIN_MM else '') for _, k, sz in cuts) + ' |')
    out['tier-strokes'] = rows
    # the measured tokens, per layout: its hero (digit height in millimetres), the hero's icon and its strip icons
    from layouts import layouts
    LAY = load_layouts()
    tier_of = {v: k for k, v in SCREEN_OF.items()}
    rows = ['| Page | Screen | Hero group | Hero | Hero icon | Strip icons (hour / day) | Digit height | mm |', '|---|---|---|---|---|---|---|---|']
    order = lambda l: (list(REG['pages']).index(l['page']), REG['screens'].index(l['screen']))
    for l in sorted(layouts(), key=order):
        e = LAY.get(l['name']) or {}
        t = tier_of[l['screen']]
        for k, ver in (('heroAlone', 'on its own'), ('heroShared', 'beside other content')):
            h = (e.get('type') or {}).get(k)
            if not h:
                continue
            d = hup[str(h)] + hdn[str(h)] + 1 if str(h) in hup else hup[h] + hdn[h] + 1
            ic = e['icon']
            icon = f"{ic['heroAloneSteps'][0]} → {ic['heroAloneSteps'][-1]}" if k == 'heroAlone' else str(ic['heroShared'])
            strips = f"{ic['stripHour'] or '—'} / {ic['stripDay']}" if ic.get('stripDay') else '—'
            rows.append(f"| {REG['pages'][l['page']]['name']} | {SCREEN[t]} | {ver} | {h} px | {icon} | {strips} | {d} px | {d * T[t]['pitch']:.1f} |")
    out['tier-hero'] = rows
    # line weights per tier: the base line and the data line (series)
    rows = header()
    for k in ('base', 'series'):
        rows.append(f'| `line.{k}` | ' + ' | '.join(f"{T[t]['line'][k]} px" for t in TIERS) + ' |')
    out['tier-line'] = rows
    # the tiers: key, screen, active area (the panel facts)
    rows = ['| Key | Screen | Active area |', '|---|---|---|']
    for t in TIERS:
        W, H, Wmm, Hmm = KNOWN[t]
        rows.append(f"| `{t}` | {SCREEN[t]}" + (f' ({ALSO[t]})' if t in ALSO else '') + f" | {Wmm:g} × {Hmm:g} mm |")
    out['tier-keys'] = rows
    return out


if __name__ == '__main__':
    for k, v in tables().items():
        print(k); print(v); print()
