#!/usr/bin/env python3
"""Values inside the design system's typed text: `<!-- v:NAME -->value<!-- /v -->` (CLAUDE.md ground rules).

The rule text around a marker is typed; the value between the markers is written by `registry.py write` from its home
here, so it can't drift. `value(name)` gives the text for a name; an unknown name is a lint error.

Names:
  dt:CONST            a constant of lib/derive_tokens.py (a style choice or threshold), as written in prose
  pct:CONST           the same constant as a percentage
  heroLadder, iconLadder, strokes.KEY, xs.SIZE, s.SIZE, unitGap.SIZE, unitGapNone, grays, tightScreens, tightRange,
  classScreens.CLASS, mediumMm, largeMm   computed from those constants and the panel facts
  input:PAGE:INPUT    an input's default in pages/PAGE.yaml, with its unit
  shared:INPUT        the default of an input every blueprint has (pages/_shared.yaml), with its unit
  layout:KEY:PATH     a measured token of one layout (ep_tokens.jinja EP_LAYOUT), e.g. layout:weather_41:icon.stripDay
  const:PAGE:SCREEN:NAME   a constant a page definition gives one of its layouts
  spec:LAYOUT:NAME    a constant of specs/LAYOUT.py (or specs/_wx.py as spec:_wx:NAME)
  order:LAYOUT        the order in which a weather layout's detail rows make way (its spec's ROW_NAMES and ORDER), in words
  color:PATH          a colour role value (lib/derive_tokens.py COLOR, a dotted path), in backticks
  heroMinUsed, heroStepPct   the smallest hero any tier uses (the tokens), the ladder's step below 160
  markerDisc          icon.markerDisc for the inline icon sizes in use
  inputPages:INPUT    the live pages whose definition has that input
  stalePages          the live pages that have a stale state
  noStalePages        the live pages that have none
  noThresholdPages    the live pages without a threshold input (flag_, warning_ or severe_)
  uses:KEY[,KEY]      the live pages that use one of these patterns or versions (registry.yaml `uses`, e.g. uses:glance,glance/footer)
  mm:TIER:SIZE:x|cap[:DECIMALS]   a TRMNL cut's x-height or cap height on a tier, in millimetres (1 decimal unless given)
  dv:WxHxWMMxHMM:PATH a token the generator derives for a screen that has no tier yet (space.pad, type.data, icon.min,
                      line.base, pitch, sizeClass); a type token reads as TRMNL<size>
  heroIconMin         the smallest icon on its own, as a fraction of the digit height
"""
import pathlib, sys
LIB = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(LIB))
import derive_tokens as dt          # noqa: E402

SRC = LIB.parent


def num(v):
    """a number as prose writes it: 1.3, 40, 0.25"""
    return str(v)


def ladder(sizes):
    """a ladder as runs: '16 · 20 · 24, then multiples of 8 to 160, then multiples of 32 to 320'"""
    runs, i = [], 0
    while i < len(sizes):
        j = i
        while j + 2 < len(sizes) and sizes[j + 1] - sizes[j] == sizes[j + 2] - sizes[j + 1]:
            j += 1
        if j - i >= 2:                      # a run is at least four rungs; shorter ones are listed
            runs.append((sizes[i], sizes[j + 1], sizes[i + 1] - sizes[i])); i = j + 2
        else:
            runs.append((sizes[i], None, None)); i += 1
    out, loose = [], []
    for a, b, step in runs:
        if b is None:
            loose.append(str(a))
            continue
        if loose:
            out.append(' · '.join(loose)); loose = []
        out.append(f'multiples of {step} from {a} to {b}' if not out else f'multiples of {step} to {b}')
    if loose:
        out.append(' · '.join(loose))
    return ', then '.join(out)


def width_mm(key):
    W, H, Wmm, Hmm = dt.KNOWN[key]
    return Wmm


def screen_name(key):
    from layouts import registry
    r = registry()
    return r['screen_names'][dt.SCREEN_OF[key]]


def tight():
    """the tiers whose canvas is narrower than TIGHT_MM, and the widest of them / the narrowest other"""
    t = sorted((width_mm(k), k) for k in dt.KNOWN if width_mm(k) < dt.TIGHT_MM)
    w = sorted(width_mm(k) for k in dt.KNOWN if width_mm(k) >= dt.TIGHT_MM)
    return t, w


def page_def(page):
    import pages
    return pages.load(page)


def input_default(page, name):
    for i in page_def(page)['inputs']:
        if i['name'] == name:
            d, sel = i.get('default'), i.get('selector') or {}
            if isinstance(d, list):
                return ', '.join(f'`{x}`' for x in d) if d else 'none (empty list)'
            unit = (sel.get('number') or {}).get('unit_of_measurement', '')
            return num(d) + ('' if not unit or unit == '°' else ' ') + unit
    raise KeyError(f'{page}: no input {name}')


def input_pages(name):
    from layouts import registry
    r = registry()
    out = []
    for page, v in r['pages'].items():
        f = SRC / 'pages' / f'{page}.yaml'
        if v.get('blueprints') and f.exists() and any(i['name'] == name for i in page_def(page).get('inputs') or []):
            out.append(v['name'])
    return ', '.join(out)


def stale_pages():
    """the live pages that have a stale state (their definition names what counts as their newest report)"""
    from layouts import registry
    return ', '.join(v['name'] for page, v in registry()['pages'].items()
                     if v.get('blueprints') and (SRC / 'pages' / f'{page}.yaml').exists() and page_def(page).get('stale'))


def live_pages():
    """[(page, registry entry, page definition)] of the pages a blueprint is built from, in the registry's order"""
    from layouts import registry
    return [(page, v, page_def(page)) for page, v in registry()['pages'].items()
            if v.get('blueprints') and (SRC / 'pages' / f'{page}.yaml').exists()]


def has_thresholds(d):
    return any(i['name'].startswith(('flag_', 'warning_', 'severe_')) for i in d.get('inputs') or [])


def class_screens(cls):
    keys = [k for k in dt.KNOWN if dt.derive(*dt.KNOWN[k])[0]['sizeClass'] == cls]
    seen = []
    for k in keys:
        n = screen_name(k).split(' ')[0]
        if n not in seen:
            seen.append(n)
    return ', '.join(seen)


def value(name):
    kind, _, arg = name.partition(':')
    if kind == 'dt':
        return num(getattr(dt, arg))
    if kind == 'pct':
        return f'{getattr(dt, arg) * 100:g}'
    if kind == 'input':
        page, inp = arg.split(':')
        return input_default(page, inp)
    if kind == 'mm':           # a cut's x-height or cap height on one tier, in millimetres
        tier, size, part, *dec = arg.split(':')
        W, H, wmm, hmm = dt.KNOWN[tier][:4]
        pitch = (wmm / W + hmm / H) / 2      # as the tier tables: both axes averaged (derive_tokens)
        return f"{dt.TRMNL[int(size)][part] * pitch:.{int(dec[0]) if dec else 1}f}"
    if kind == 'stalePages':
        return stale_pages()
    if kind == 'noStalePages':
        return ', '.join(v['name'] for _, v, d in live_pages() if not d.get('stale'))
    if kind == 'noThresholdPages':
        return ', '.join(v['name'] for _, v, d in live_pages() if not has_thresholds(d))
    if kind == 'uses':
        got = ', '.join(v['name'] for _, v, _ in live_pages() if v.get('uses') in arg.split(','))
        if not got:
            raise KeyError(arg)
        return got
    if kind == 'shared':
        import pages
        i = pages.shared()['inputs'][arg]
        unit = ((i.get('selector') or {}).get('number') or {}).get('unit_of_measurement', '')
        return num(i['default']) + ((' ' + unit) if unit else '')
    if kind == 'layout':
        from tier_tables import load_layouts
        key, path = arg.split(':')
        v = load_layouts()[key]
        for k in path.split('.'):
            v = v[k]
        return num(v)
    if kind == 'const':
        page, screen, n = arg.split(':')
        return num(page_def(page)['layouts'][screen]['constants'][n])
    if kind == 'order':
        import importlib.util
        sys.path.insert(0, str(SRC / 'specs'))
        sp = importlib.util.spec_from_file_location(arg, SRC / 'specs' / f'{arg}.py')
        m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
        words = {'rain': 'rain', 'wind': 'wind', 'hum': 'humidity', 'hilo': 'high/low', 'pres': 'pressure', 'rise': 'sunrise', 'set': 'sunset'}
        return ', '.join(words[m.ROW_NAMES[i]] for i in m.ORDER)
    if kind == 'spec':
        import importlib.util
        key, n = arg.split(':')
        sys.path.insert(0, str(SRC / 'specs'))
        sp = importlib.util.spec_from_file_location(key, SRC / 'specs' / f'{key}.py')
        m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
        return num(getattr(m, n))
    if kind == 'color':
        v = dt.COLOR
        for k in arg.split('.'):
            v = v[k]
        return f'`{v}`'
    if kind == 'dv':
        dims, path = arg.split(':')
        d = dt.derive(*[float(x) if '.' in x else int(x) for x in dims.split('x')])[0]
        v = d
        for k in path.split('.'):
            v = v[k]
        return f'TRMNL{v[1]}' if isinstance(v, list) else num(v)
    if name == 'heroIconMin':
        return f'{dt.HERO_ICON_MIN[0]}/{dt.HERO_ICON_MIN[1]}'
    if kind == 'inputPages':
        return input_pages(arg)
    head, _, key = name.partition('.')
    if name == 'markerDisc':
        ins = sorted({dt.derive(*dt.KNOWN[k])[0]['icon']['inline'] for k in dt.KNOWN})
        return ', '.join(f'{i // 2 + 1} at {i} px' for i in ins)
    if name == 'heroMinUsed':
        from tier_tables import load_layouts
        return str(min(v for e in load_layouts().values() for k in ('heroAlone', 'heroShared') for v in [e['type'][k]] if v))
    if name == 'heroStepPct':
        eight = [x for x in dt.HERO_SIZES if x <= 160]
        return f'{8 / eight[-2] * 100:.0f}–{8 / eight[0] * 100:.0f} %'
    if name == 'heroLadder':
        return ladder(dt.HERO_SIZES)
    if name == 'iconLadder':
        return ladder(dt.ICON_LADDER)
    if head == 'strokes':
        v = dt.STROKES[key]
        return f'{v[0]} on / {v[1]} off' if isinstance(v, list) else str(v)
    if head in ('xs', 's'):
        return str((dt.XS if head == 'xs' else dt.S)[int(key)])
    if head == 'unitGap':
        from gen_tokens import unit_gap
        return str(unit_gap()[key])
    if name == 'unitGapNone':
        return ', '.join(f'`{u}`' for u in dt.UNIT_GAP_NONE)
    if name == 'grays':
        return f"`{dt.COLOR['severe']['gray']['severe']}` and `{dt.COLOR['warning']['gray']['warning']}`"
    if name == 'tightScreens':
        t, _ = tight()
        return ', '.join(f'{screen_name(k)} {num(w)} mm' for w, k in t)
    if name == 'tightRange':
        t, w = tight()
        return f'above {num(t[-1][0])} mm up to {num(w[0])} mm'
    if head == 'classScreens':
        return class_screens(key)
    raise KeyError(name)


if __name__ == '__main__':
    for n in sys.argv[1:]:
        print(n, '=', value(n))
