#!/usr/bin/env python3
"""Derive a screen's design tokens from its resolution and active area (design system: Token register).

usage: derive_tokens.py                 check: derive the known tiers and compare with ep_tokens.jinja
       derive_tokens.py W H Wmm Hmm      derive one screen, print its tokens and which tier it belongs to

Tier keys name what sets the tokens: canvas pixels (after rotation) and pixel pitch, "800x480-0.20". A screen
belongs to an existing tier when its derived tokens equal that tier's; the key only labels the result, so the
inch size on the box and the rounding of the pitch never decide the tier.

Kinds (see the register): panel facts are the inputs; floors come from the thresholds below applied to the
pixel pitch; derived tokens follow from other tokens; large screens step up one size; style choices are copied.
Measured tokens (hero sizes, strip icons, detail column) depend on a layout and are only given as floors.
"""
import json, math, pathlib, sys

LIB = pathlib.Path(__file__).parent

# ---- style choices (the register's thresholds and constants) ----
PAD_SHARE, PAD_MIN_MM = 0.05, 1.3          # padding: 5 % of the short side, at least 1.3 mm
RULE_MIN_MM = 0.15                          # a 1 px rule needs 1 px >= 0.15 mm, else 2 px
STROKE_MIN_MM = 0.25                        # stems and icon strokes
X_DATA_MM, X_LABEL_MM, X_CAPS_ONLY_MM = 1.3, 1.0, 1.1
GLANCE_DIGITS_MM = 7.5
NATIVE_TOL_MM = 0.05                        # a native cut is preferred over a 2x cut while within 0.05 mm of the floor
# size classes by the short side: small < 35 mm, medium 35-80 mm (type.primary), large > 80 mm (type.primary + one step up)
MEDIUM_SHORT_MM, LARGE_SHORT_MM = 35, 80
TITLE_BASE = 16                             # the title is chrome: TRMNL16 Bold unless the label floor is higher
ICON_LADDER = [16, 20, 24] + list(range(32, 161, 8)) + list(range(192, 321, 32))   # the icon ladder
HERO_SIZES = list(range(56, 161, 8)) + list(range(192, 321, 32))   # the hero ladder (lib/hero_metrics.py)
# strokes as multiples of line.base (tick, heavy, bar gap; dash and dot on/off); a data series is line.base + SERIES_UP,
# one more on a large screen
STROKES = {'tick': 3, 'dash': [4, 4], 'dot': [1, 1], 'forecastDash': [6, 3], 'heavy': 4, 'barGap': 2}
SERIES_UP = 1
TIME_TICKS = 5                              # a clock-time chart axis: labels evenly spaced, both ends included
TIGHT_MM = 40                               # a canvas narrower than this attaches units to their value
UNIT_GAP_NONE = ['%', 'C', 'F', 'h', 'min', 'am', 'pm']   # symbols that attach to their value on every screen
HERO_GAP_DIV = 7                            # space.heroGap and the hero clearance: hero size / 7
# the Hero group rule: the icon's glyph height is at most K x the digit height (beside other content / on its own); on its
# own it steps down to the smallest icon whose glyph height is at least MIN (a fraction) of the digit height
HERO_ICON_K, HERO_ICON_K_ALONE, HERO_ICON_MIN = 1, 1.2, (2, 3)
CHART_TOP = 1.5                             # a chart with thresholds runs up to 1.5 x the severe value
QR_MODULE_MM = 0.4                          # the smallest QR module a phone reads at arm's length (Code; no layout yet)
HERO_FONT = 'SpaceGrotesk-Bold'
# colour roles per panel capability (*Values per panel*): severe by the panel's colours, warning a fill only where red and
# yellow are both there (or a gray), else an outlined chip; the grays are the 4-gray panel's own middle levels
COLOR = {
    'ink': 'black', 'paper': 'white',
    'severe': {'red': {'severe': 'red', 'onSevere': 'white', 'severeMark': ''},
               'yellow': {'severe': 'yellow', 'onSevere': 'black', 'severeMark': ''},
               'gray': {'severe': '#555555', 'onSevere': 'white', 'severeMark': ''},
               'mono': {'severe': 'black', 'onSevere': 'white', 'severeMark': ''}},
    'warning': {'red_yellow': {'warning': 'yellow', 'onWarning': 'black', 'chip': 'yellow'},
                'gray': {'warning': '#aaaaaa', 'onWarning': 'white', 'chip': '#aaaaaa'},
                'mono': {'warning': 'black', 'onWarning': 'black', 'chip': 'outline'}},
}

# ---- TRMNL metrics: native cuts 12 / 16 / 21 and their exact 2x cuts 24 / 32 / 42 ----
# size: x-height, cap height (CAPUP + CAPDN + 1), Regular stem, Bold stem, font key Regular / Bold
TRMNL = {
    12: dict(x=6, cap=8, r=1, b=2, fr='unit12', fb='label12'),
    16: dict(x=8, cap=11, r=1, b=2, fr='unit16', fb='label16'),
    21: dict(x=11, cap=15, r=2, b=3, fr='text21', fb='strong21'),
    24: dict(x=12, cap=16, r=2, b=4, fr='unit12x2', fb='label12x2'),
    32: dict(x=16, cap=22, r=2, b=4, fr='unit16x2', fb='label16x2'),
    42: dict(x=22, cap=30, r=4, b=6, fr='text21x2', fb='strong21x2'),
}
SIZES = sorted(TRMNL)
NATIVE = [12, 16, 21]
# text-bound space: XS / S around a size (2/4 around 12-16, 3/6 around 21; a 2x cut doubles its base)
XS = {12: 2, 16: 2, 21: 3, 24: 4, 32: 4, 42: 6}
S = {12: 4, 16: 4, 21: 6, 24: 8, 32: 8, 42: 12}


def font_files():
    """font.*: each TRMNL cut's file (a 2x cut draws its base size's file) and the hero face"""
    out = {}
    for size in NATIVE + [x for x in SIZES if x not in NATIVE]:
        base = size if size in NATIVE else size // 2
        for w, file in (('fb', 'Bold'), ('fr', 'Regular')):
            out[TRMNL[size][w]] = f'TRMNL{base}-{file}.ttf'
    out['hero'] = HERO_FONT + '.ttf'
    return out


def step(size, n=1):
    i = SIZES.index(size) + n
    return SIZES[max(0, min(i, len(SIZES) - 1))]


def derive(W, H, Wmm, Hmm):
    pitch = ((Wmm / W) + (Hmm / H)) / 2
    short_px, short_mm = min(W, H), min(Wmm, Hmm)
    large = short_mm > LARGE_SHORT_MM
    medium_up = short_mm >= MEDIUM_SHORT_MM
    out, notes = {'width': W, 'height': H, 'pitch': round(pitch, 3)}, []

    # floors
    pad = max(PAD_SHARE * short_px, PAD_MIN_MM / pitch)
    pad = int(math.floor(pad / 2 + 0.5)) * 2
    rule = 1 if pitch >= RULE_MIN_MM else 2
    def floor_size(floor):
        """The smallest cut whose x-height meets the floor. When that is a 2x cut, the native cut below it is
        preferred while its x-height is within NATIVE_TOL_MM of the floor: a drawn glyph reads better than a doubled
        one. Between two native cuts the floor holds exactly."""
        s = next(s for s in SIZES if TRMNL[s]['x'] * pitch >= floor)
        below = [n for n in NATIVE if n < s]
        if s not in NATIVE and below and TRMNL[below[-1]]['x'] * pitch >= floor - NATIVE_TOL_MM:
            notes.append(f'TRMNL{below[-1]} native for x-height floor {floor} mm: {TRMNL[below[-1]]["x"] * pitch:.2f} mm, '
                         f'within {NATIVE_TOL_MM} mm (TRMNL{s} would be the 2x cut)')
            return below[-1]
        return s

    data = floor_size(X_DATA_MM)
    label = floor_size(X_LABEL_MM)
    # only TRMNL12's lowercase is too small: it counts for labels in capitals only under 1.1 mm
    caps_only = label == 12 and TRMNL[label]['x'] * pitch < X_CAPS_ONLY_MM
    icon_min = next(i for i in ICON_LADDER if i / 12 * pitch >= STROKE_MIN_MM)
    from hero_metrics import measure                 # the digits' measured ink height
    glance_floor = next(h for h in HERO_SIZES if (lambda m: m[1] + m[2] + 1)(measure(h)) * pitch >= GLANCE_DIGITS_MM)
    ok_regular = lambda s: TRMNL[s]['r'] * pitch >= STROKE_MIN_MM
    ok_bold = lambda s: TRMNL[s]['b'] * pitch >= STROKE_MIN_MM

    # step up on large screens
    if large:
        data, label = step(data), step(label)
        caps_only = False
    title = max(TITLE_BASE, label)
    if large:
        title = step(title)
    stamp = max(step(title, -1), label)
    unit = max(step(data, -1), label if not caps_only else step(label))
    field = step(label) if large else label
    field_cut = 'r' if (large and ok_regular(field)) else 'b'
    primary = step(data) if medium_up else None
    if primary and primary > 21 and data <= 21:
        primary = 21            # a step up from native data stays native: TRMNL21 is the largest drawn cut
    # the line under a Glance hero: one native step above type.data, at most TRMNL21, never below type.data; Bold
    secondary = max(data, min(step(data), 21))
    # an inline icon is as tall as the text beside it: the smallest ladder size >= type.data, never below icon.min
    icon_inline = max(icon_min, next(i for i in ICON_LADDER if i >= data))
    for s, kind in ((data, 'data'), (label, 'label'), (title, 'title')):
        if not ok_bold(s):
            notes.append(f'{kind} {s}: even the Bold cut is under {STROKE_MIN_MM} mm')
    used = sorted({x for x in (data, label, title, stamp, unit, field, primary or 12) if x not in NATIVE})
    if used:
        notes.append('uses the 2x cuts ' + ', '.join(f'TRMNL{x} (TRMNL{x // 2} at 2x)' for x in used))
    if primary and not ok_regular(primary):
        notes.append(f'type.primary {primary}: the Regular cut is under {STROKE_MIN_MM} mm, so both cuts are Bold')

    def cut(size, c):
        return TRMNL[size]['fb' if c == 'b' else 'fr']

    out['space'] = {'pad': pad, 'm': pad // 2, 'l': pad}
    cap = lambda s: TRMNL[s]['cap']
    out['space']['titleRow'] = cap(title) + S[title] + rule
    row_min = cap(data) + 2 * XS[data] + 1
    out['space']['row'] = row_min + 2 * S[data]
    out['space']['rowDense'] = row_min + S[data] + XS[data]
    out['space']['detailRow'] = row_min + XS[data]
    out['space']['footer'] = rule + S[data] + cap(data)
    out['space']['axis'] = STROKES['tick'] * rule + S[label] + cap(label)   # line.tick + space.s + caps
    out['type'] = {
        'title': [cut(title, 'b'), title], 'stamp': [cut(stamp, 'b'), stamp],
        'label': [cut(label, 'b'), label] + (['caps only'] if caps_only else []),
        'fieldLabel': [cut(field, field_cut), field],
        'data': [cut(data, 'b'), data], 'unit': [cut(unit, 'r'), unit], 'secondary': [cut(secondary, 'b'), secondary],
        'primary': ([[cut(primary, 'r' if ok_regular(primary) else 'b'), primary], [cut(primary, 'b'), primary]] if primary else None),
        'heroAlone floor': glance_floor,
    }
    out['icon'] = {'min': icon_min, 'inline': icon_inline, 'markerDisc': icon_inline // 2 + 1}
    out['line'] = {'base': rule, 'series': rule + SERIES_UP + (1 if large else 0)}
    out['sizeClass'] = 'large' if large else ('medium' if medium_up else 'small')
    return out, notes


def step_icon(i):
    return ICON_LADDER[min(ICON_LADDER.index(i) + 1, len(ICON_LADDER) - 1)]


def tier_key(W, H, Wmm, Hmm):
    """The tier's name: canvas pixels and pixel pitch (mm, 0.01)."""
    return f'{W}x{H}-{((Wmm / W) + (Hmm / H)) / 2:.2f}'


# the tiers we have: canvas after rotation and active area (mm), as the firmware reports them
KNOWN = {'200x200-0.13': (200, 200, 26, 26), '384x168-0.17': (384, 168, 62, 29), '168x384-0.17': (168, 384, 29, 62),
         '384x184-0.21': (384, 184, 80, 38), '400x300-0.21': (400, 300, 84, 63), '800x480-0.20': (800, 480, 163.2, 97.92),
         '480x800-0.20': (480, 800, 97.92, 163.2),
         '800x480-0.12': (800, 480, 92.8, 55.68)}
# each tier's screen (registry.yaml screen_names), and what else is known about its panels (the Tiers table)
SCREEN_OF = {'200x200-0.13': '14', '384x168-0.17': '27l', '168x384-0.17': '27p', '384x184-0.21': '35', '400x300-0.21': '41',
             '800x480-0.20': '75', '480x800-0.20': '75p', '800x480-0.12': '426'}
ALSO = {'400x300-0.21': 'also the Seeed EN05 "4.1" MONO"', '800x480-0.20': 'the 7.3" Spectra panels derive the same tokens',
        '800x480-0.12': 'the Seeed 4.26" kit, reports `4.3" MONO`'}


def tokens():
    import jinja2
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(str(LIB)))
    return json.loads(env.from_string("{% from 'ep_tokens.jinja' import EP_TIER %}{{ EP_TIER | tojson }}").render())


def diff(d, tk):
    """(name, derived, token) for every compared token that differs."""
    pairs = [(f'space.{k}', d['space'][k], tk['space'].get(k)) for k in ('pad', 'm', 'l', 'titleRow', 'footer', 'axis', 'row', 'detailRow', 'rowDense')]
    pairs += [(f'type.{k}', d['type'][k][:2] if d['type'][k] else None, tk['type'][k]) for k in ('title', 'stamp', 'label', 'fieldLabel', 'data', 'unit', 'secondary')]
    pairs += [('type.primary', d['type']['primary'], tk['type']['primary'])]
    pairs += [(f'icon.{k}', d['icon'][k], tk['icon'][k]) for k in ('min', 'inline', 'markerDisc')]
    pairs += [('line.base', d['line']['base'], tk['line']['base'])]
    pairs += [('canvas', [d['width'], d['height']], [tk['width'], tk['height']])]
    out = []
    for name, got, want in pairs:
        if want is None and name in ('space.detailRow', 'space.rowDense', 'type.fieldLabel', 'type.primary'):
            continue        # the tier doesn't use it: nothing to compare
        if got != want:
            out.append((name, got, want))
    return out


def match(W, H, Wmm, Hmm):
    """The existing tier whose tokens this screen derives, or None (a new tier)."""
    d, _ = derive(W, H, Wmm, Hmm)
    return next((t for t, tk in tokens().items() if not diff(d, tk)), None)


def check():
    T = tokens()
    bad = 0
    for t in T:
        if t not in KNOWN:
            bad += 1
            print(f'{t}: in ep_tokens.jinja but no panel facts here')
    for t, args in KNOWN.items():
        if tier_key(*args) != t:
            bad += 1
            print(f'{t}: the panel facts give the key {tier_key(*args)}')
        d, notes = derive(*args)
        tk = T[t]
        for name, got, want in diff(d, tk):
            bad += 1
            print(f'{t:13} {name:16} derived {got!s:28} token {want}')
    print(f'{len(KNOWN)} tiers checked, {bad} differences')
    return bad


if __name__ == '__main__':
    if len(sys.argv) == 5:
        a = (int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]))
        d, notes = derive(*a)
        print(json.dumps(d, indent=1))
        for n in notes:
            print('NOTE:', n)
        t = match(*a)
        print(f'TIER: {t} (same tokens)' if t else f'TIER: none yet, a new tier would be {tier_key(*a)}')
    else:
        sys.exit(1 if check() else 0)
