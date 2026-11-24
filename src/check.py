#!/usr/bin/env python3
"""Design-system pixel check for the blueprints.

Builds nothing itself: point it at a build output folder. For every case it renders the
scenario through harness.py, then measures each payload element on its own (ink box, with
descenders ignored for the bottom edge) and checks the layout against the tier values:

  title   title caps start at P (top and left); the title rule sits at P + TH - rule width
  edges   all ink stays inside the padding; fills may enter it as far as a chip hangs (S, and an outline one line.base more)
  gap     (gap='M') the first ink below the title rule starts exactly M below it; (gap='M+') at M or lower: a chart on the
          automatic scale, whose top label gives way to a threshold label close to it (the plot still starts at M)
  bottom  (bottom='fill') the lowest ink ends exactly on row H - P - 1
  group   a hero group (number, its icon, the moon badge) keeps space.l (= P) from any text it shares rows with
  badge   the moon badge's paper ring never cuts a rule
  overlap no text (TRMNL or hero) overlaps other text, an icon or a line
  hero    nothing drawn after a hero numeral covers it (its degree sign excepted)
  chips   every fill stays on the canvas, and text on a fill stays inside it
  same    a page keeps its layout from one state to the next: the same hero size, the same lines, the same hero icon
          size on a Hero dashboard (compared across the cases of one blueprint; pollen-less and error cases apart)

usage: check.py OUT_DIR      exit code 1 when any case fails
"""
import asyncio, copy, io, contextlib, sys, pathlib, unicodedata
import numpy as np
from PIL import Image, ImageFont
from odl_renderer import generate_image
sys.path.insert(0, str(pathlib.Path(__file__).parent))
sys.path.insert(0, str(pathlib.Path(__file__).parent / "lib"))
import harness

ROOT = pathlib.Path(__file__).parent
import atexit, os, shutil, tempfile
# this run's scratch folder: one per run (two runs at once don't share files), removed when the run ends; the processes
# a run starts find it in EP_CHECK_TMP
if not os.path.isdir(os.environ.get('EP_CHECK_TMP', '')):
    os.environ['EP_CHECK_TMP'] = tempfile.mkdtemp(prefix='epaper_check_')
    atexit.register(shutil.rmtree, os.environ['EP_CHECK_TMP'], True)
CHECK_PNG = str(pathlib.Path(os.environ['EP_CHECK_TMP']) / f'{os.getpid()}.png')    # each process draws into its own file
FONTS = str(ROOT / 'fonts')
def tier_vals(bp):
    """the layout's P, TH (title row), M, line width and chip overhang S, from the tokens of the package being checked (EP_CT):
    its tier is its blueprint's screen's (derive_tokens.SCREEN_OF); S is space.s around its data text"""
    import os, json, jinja2
    from registry import screen_of
    from derive_tokens import SCREEN_OF, S as S_OF
    path = pathlib.Path(os.environ.get('EP_CT') or ROOT / 'lib') / 'ep_tokens.jinja'
    if path not in _TOKENS:
        _TOKENS[path] = json.loads(jinja2.Environment().from_string(path.read_text() + '{{ EP_TIER | tojson }}').render())
    e = _TOKENS[path][{v: k for k, v in SCREEN_OF.items()}[screen_of(B[bp])]]
    return (e['space']['pad'], e['space']['titleRow'], e['space']['m'], e['line']['base']), S_OF[e['type']['data'][1]]


def tier_tokens(bp):
    """every token of the layout's tier (the package being checked)"""
    from registry import screen_of
    from derive_tokens import SCREEN_OF
    tier_vals(bp)
    path = pathlib.Path(os.environ.get('EP_CT') or ROOT / 'lib') / 'ep_tokens.jinja'
    return _TOKENS[path][{v: k for k, v in SCREEN_OF.items()}[screen_of(B[bp])]]


FONT_FILES = {'TRMNL12-Regular.ttf': 12, 'TRMNL12-Bold.ttf': 12, 'TRMNL16-Regular.ttf': 16, 'TRMNL16-Bold.ttf': 16,
              'TRMNL21-Regular.ttf': 21, 'TRMNL21-Bold.ttf': 21}
FILLS = {'black', 'white', 'red', 'yellow', '#555555', '#aaaaaa'}


def universal(bp, payload):
    """The rules that hold on every screen of every page, each written from its sentence in the design system (named in
    brackets). They are checked on every case, so a new page can't break them unseen."""
    import re
    from derive_tokens import HERO_SIZES, ICON_LADDER
    e = tier_tokens(bp)
    P, TH = e['space']['pad'], e['space']['titleRow']
    base = e['line']['base']
    dashes = {tuple(e['line'][k]) for k in ('dash', 'dot', 'forecastDash')}
    errs = set()
    for el in payload:
        ty = el.get('type')
        if any(isinstance(el.get(k), str) and el[k].strip().endswith('%') for k in ('x', 'y', 'x_start', 'y_start', 'x_end', 'y_end')):
            errs.add(f'a position in percent ({ty}) [*Positioning*]')
        if ty == 'text':
            font = str(el.get('font') or '').split('/')[-1]
            size, val = el.get('size'), str(el.get('value', ''))
            if not font:
                errs.add(f'text {val[:12]!r} has no font [*Blueprint mechanics*]')
            elif font in FONT_FILES:
                if size not in (FONT_FILES[font], 2 * FONT_FILES[font]):
                    errs.add(f'{font} drawn at {size} px [*Typography*, *Never scale off-size*]')
                if 'Regular' in font and FONT_FILES[font] < 21 and not re.fullmatch(r'[A-Za-zµΩ°%€$£][A-Za-zµΩ°%€$£0-9/·-]{0,9}', val):
                    errs.add(f'{font} for {val[:14]!r}, which is no unit [*Physical size minimums*: TRMNL12 and TRMNL16 text is always Bold, a unit excepted]')
            elif font == 'SpaceGrotesk-Bold.ttf':
                if size not in HERO_SIZES:
                    errs.add(f'hero text at {size} px, off the hero ladder [*Style choices*, *Hero ladder*]')
            elif font == 'materialdesignicons-webfont.ttf':
                if size not in ICON_LADDER:
                    errs.add(f'icon at {size} px, off the icon ladder [*How to draw them*, *Size ladder*]')
            else:
                errs.add(f'font {font} [*Typography*, *No other fonts*]')
            if el.get('color') not in ('black', 'white'):
                errs.add(f"text {val[:12]!r} in {el.get('color')} [*Values per panel*, *Warning and severe are fills only*, and gray is never text]")
            # the update stamp: the right-aligned text of the title row
            y = el.get('y')
            if isinstance(y, (int, float)) and y < P + TH and str(el.get('anchor', '')).startswith('r') and font in FONT_FILES:
                if not re.fullmatch(r'(! )?[^\W\d_]{2} \d{1,2}:\d{2}( [AP]M)?', val):
                    errs.add(f'update stamp {val!r} [*Title row*, *Update stamp*]')
        elif ty == 'line':
            if el.get('fill') not in ('black', 'white'):
                errs.add(f"a line in {el.get('fill')} [*Values per panel*, *Gray is a fill, never text or a line*]")
            if int(el.get('width', 1)) not in (1, base, e['line']['heavy']):
                errs.add(f"a line {el.get('width')} px wide [*Lines and strokes*: every stroke follows line.base]")
            if el.get('dashed') and (el.get('dash_length'), el.get('space_length')) not in dashes:
                errs.add(f"a dash of {el.get('dash_length')} on / {el.get('space_length')} off [*Lines and strokes*: line.dash, line.dot, line.forecastDash]")
        elif ty in ('rectangle', 'polygon', 'circle', 'ellipse'):
            for k in ('fill', 'outline'):
                if el.get(k) is not None and el[k] not in FILLS:
                    errs.add(f"a {ty} {k} of {el[k]} [*Values per panel*: only the panel's colours]")
            if ty in ('rectangle', 'circle', 'ellipse') and el.get('outline') is not None and el.get('outline') != el.get('fill') \
                    and int(el.get('width', 1)) not in (base, 2 * base, 2 * base + 1):
                errs.add(f"an outline {el.get('width')} px wide [*Chips*: an outline of 2 x line.base; *Spacing (internal)*, *Chips hang outward*: a hero's inside its box]")
        elif ty == 'icon':            # the renderer's own icon element, for an icon the kit has no glyph for (*Blueprint mechanics*)
            if el.get('color', 'black') not in ('black', 'white'):
                errs.add(f"an icon in {el.get('color')} [*How to draw them*, *Colour*]")
        else:
            errs.add(f'an element of type {ty!r}, which the kit does not draw with [*Blueprint mechanics*]')
    return sorted(errs)


def universal_selftest(bp):
    """each system-wide rule fires on a drawing that breaks it: a check that can't fail proves nothing"""
    good = {'type': 'text', 'font': 'TRMNL16-Bold.ttf', 'size': 16, 'color': 'black', 'value': 'OK', 'x': 50, 'y': 100, 'anchor': 'lm'}
    bad = {'no font': dict(good, font=''), 'off-size': dict(good, size=17), 'no unit': dict(good, font='TRMNL16-Regular.ttf', value='Kitchen 21'),
           'hero ladder': dict(good, font='SpaceGrotesk-Bold.ttf', size=100), 'icon ladder': dict(good, font='materialdesignicons-webfont.ttf', size=30),
           'other fonts': dict(good, font='Arial.ttf'), 'gray is never text': dict(good, color='red'), 'Update stamp': dict(good, value='Sat 14:10', y=5, anchor='rm'),
           'in percent': dict(good, x='50%'),
           'never text or a line': {'type': 'line', 'fill': '#aaaaaa', 'width': 1, 'x_start': 0, 'x_end': 9, 'y_start': 5, 'y_end': 5},
           'follows line.base': {'type': 'line', 'fill': 'black', 'width': 7, 'x_start': 0, 'x_end': 9, 'y_start': 5, 'y_end': 5},
           'line.dash': {'type': 'line', 'fill': 'black', 'width': 1, 'dashed': True, 'dash_length': 5, 'space_length': 2, 'x_start': 0, 'x_end': 9, 'y_start': 5, 'y_end': 5},
           "only the panel's colours": {'type': 'rectangle', 'fill': 'blue', 'outline': 'blue', 'x_start': 0, 'x_end': 9, 'y_start': 5, 'y_end': 9},
           'an outline': {'type': 'rectangle', 'outline': 'black', 'width': 9, 'x_start': 0, 'x_end': 9, 'y_start': 5, 'y_end': 9},
           'an icon in': {'type': 'icon', 'value': 'mdi:home', 'color': 'red', 'x': 5, 'y': 5, 'size': 24},
           'does not draw with': {'type': 'multiline', 'value': 'a|b', 'x': 5, 'y': 5}}
    if universal(bp, [good]):
        return [f'the system-wide rules reject a correct text: {universal(bp, [good])}']
    return [f'the system-wide rule "{k}" does not fire on a drawing that breaks it' for k, el in bad.items() if not any(k in e for e in universal(bp, [el]))]


def footer_height(bp):
    """space.footer of the layout's tier (the footer's line is that far above the bottom padding)"""
    import os
    from registry import screen_of
    from derive_tokens import SCREEN_OF
    path = pathlib.Path(os.environ.get('EP_CT') or ROOT / 'lib') / 'ep_tokens.jinja'
    return _TOKENS[path][{v: k for k, v in SCREEN_OF.items()}[screen_of(B[bp])]]['space']['footer']


_TOKENS = {}

sys.path.insert(0, str(ROOT / 'lib'))
# the one list of check cases, (scenario, blueprint, gap rule, bottom rule); gap 'skip': centred Glance, charts, row
# layouts, error blocks. Each layout's kinds of state are listed in lib/coverage.py.
from pixcmp_cases import B, CASES, EXTRA_CASES, SIZES, CONFIG_CASES   # noqa: E402
from derive_tokens import HERO_GAP_DIV                  # noqa: E402



_desc = {}


def descenders(font, size):
    """Characters of this font that draw below the baseline."""
    key = (font, size)
    if key not in _desc:
        f = ImageFont.truetype(f'{FONTS}/{font}', size)
        chars = set()
        for c in (chr(i) for i in range(33, 0x250)):
            try:
                bb = f.getbbox(c, anchor='ls')
            except Exception:
                continue
            if bb and bb[3] > 0 and bb[2] > bb[0]:
                chars.add(c)
        _desc[key] = chars
    return _desc[key]


def ink_box(el, W, H):
    e = copy.deepcopy(el)
    for k in ('color', 'fill', 'outline'):
        if k in e and e[k] not in (None, 'white'):
            e[k] = 'black'
    if e.get('type') == 'line' and el.get('fill') == 'white':
        return None                       # paper notches: invisible by design
    if e.get('type') in ('text', 'icon'):
        e['color'] = 'black'                  # text and icons on a dark chip are white: measure them anyway
    if e.get('type') == 'rectangle' and el.get('outline') == 'white':
        e['outline'] = 'black'                # meter segments drawn on a dark chip
        if el.get('fill') == 'white':
            e['fill'] = 'black'
    img = asyncio.run(generate_image(width=W, height=H, elements=[e], background='white',
                                     accent_color='red', font_dirs=[FONTS]))
    a = np.array(img.convert('L')) < 128
    if not a.any():
        return None
    ys, xs = np.where(a.any(axis=1))[0], np.where(a.any(axis=0))[0]
    box = [int(xs[0]), int(ys[0]), int(xs[-1]), int(ys[-1])]
    if e.get('type') == 'text':          # top edge without accents (*Text rules*, *Accents hang*)
        v = str(e['value'])
        bare = ''.join(c for c in unicodedata.normalize('NFD', v) if unicodedata.category(c) != 'Mn')
        bare = unicodedata.normalize('NFC', bare)
        if bare != v:
            img1 = asyncio.run(generate_image(width=W, height=H, elements=[dict(e, value=bare)], background='white',
                                              accent_color='red', font_dirs=[FONTS]))
            a1 = np.array(img1.convert('L')) < 128
            if a1.any():
                box[1] = int(np.where(a1.any(axis=1))[0][0])
    if e.get('type') == 'text':          # bottom edge without descenders
        d = descenders(e['font'], e['size'])
        v = str(e['value'])
        if any(c in d for c in v):
            e2 = dict(e, value=''.join('x' if c in d else c for c in v))
            img2 = asyncio.run(generate_image(width=W, height=H, elements=[e2], background='white',
                                              accent_color='red', font_dirs=[FONTS]))
            a2 = np.array(img2.convert('L')) < 128
            if a2.any():
                box[3] = int(np.where(a2.any(axis=1))[0][-1])
    return box


def kind(el):
    t = el.get('type')
    if t == 'polygon':
        return 'fill'
    if t == 'rectangle' and 'fill' not in el and el.get('width', 1) >= 2:
        return 'fill'                     # an outlined warning chip: it hangs outward like any chip
    if t == 'rectangle':
        small = abs(el['x_end'] - el['x_start']) < 16 and abs(el['y_end'] - el['y_start']) < 16
        return 'fill' if el.get('fill') not in (None, 'white') and not small else 'ink'   # meter segments, markers = ink
    return 'ink'


def check(out_dir, scen, bp, gap_rule, bottom_rule, sized=False):
    sf = ROOT / 'scen' / f'{scen}.py'
    # every case is drawn at its layout's canvas size (a scenario has none of its own; a weather extra runs on several)
    tf = pathlib.Path(CHECK_PNG).with_name(f'{os.getpid()}_{bp}_{scen}.py')
    tf.write_text(f"exec(open({str(sf)!r}).read())\nSIZE={SIZES[bp]}\n")
    sf = tf
    want_ns = {}
    exec(sf.read_text(), want_ns)
    errs0 = []

    def side(errs):
        # the template triggers that fire in the case's state (a deadline: *Medication*, *Medication redraws by itself*) and the
        # devices whose LED the run flashes (*Blueprint mechanics*, *Button feedback (LED flash)*)
        if 'EXPECT_FIRES' in want_ns and sorted(set(harness.LAST['fired'])) != sorted(want_ns['EXPECT_FIRES']):
            errs.append(f"the template triggers that fire are {sorted(set(harness.LAST['fired']))}, not {sorted(want_ns['EXPECT_FIRES'])}")
        if 'EXPECT_FLASH' in want_ns and harness.LAST['led'] != want_ns['EXPECT_FLASH']:
            errs.append(f"the LED flashes on {harness.LAST['led']}, not {want_ns['EXPECT_FLASH']}")
        return errs
    # a case whose rule says nothing is drawn: the automation must stop before it draws (*Medication*, *No press, no redraw*)
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            payload = harness.run(str(pathlib.Path(out_dir) / B[bp]), str(sf), CHECK_PNG)
    except harness.NoDraw:
        if want_ns.get('EXPECT_NO_DRAW'):
            return side(errs0)
        raise
    if want_ns.get('EXPECT_NO_DRAW'):
        return side(['the blueprint draws, where this case is there to show it draws nothing'])
    W, H = Image.open(CHECK_PNG).size
    (P, TH, M, rw), S = tier_vals(bp)      # from the tokens: a canvas can belong to two tiers (800 x 480: the 7.5" and the 4.26")
    errs = side(universal(bp, payload))
    # what the case's rule says the screen shows (below the title row) or must not show (anywhere): the drawing instructions,
    # not whether the text is legible
    said = [str(el.get('value', '')) for el in payload if el.get('type') in ('text', 'multiline')]
    body = [str(el.get('value', '')) for el in payload if el.get('type') in ('text', 'multiline') and (el.get('y') or 0) >= P + TH]
    for w in want_ns.get('EXPECT') or []:
        if not any(w in v for v in body):
            errs.append(f'the screen does not show {w!r}, which this case is there to show')
    if want_ns.get('EXPECT_ICON') is False and [el for el in payload if (el.get('y') or 0) >= P + TH and (el.get('type') == 'icon'
                                                   or (el.get('type') == 'text' and 'materialdesign' in str(el.get('font', ''))))]:
        errs.append('an icon below the title row, which this case is there to rule out')
    for w in want_ns.get('EXPECT_NOT') or []:
        if any(w in v for v in said):
            errs.append(f'the screen shows {w!r}, which this case is there to rule out')
    # the only colours the case's panels share (*Values per panel*, *Not configurable*: a colour only where every selected panel has it)
    if want_ns.get('EXPECT_COLOURS'):
        used = {str(el[k]) for el in payload for k in ('color', 'fill', 'outline') if el.get(k) is not None}
        if used - set(want_ns['EXPECT_COLOURS']):
            errs.append(f"colours {sorted(used - set(want_ns['EXPECT_COLOURS']))} that not every panel of this case has")
    items = [(el, kind(el), ink_box(el, W, H)) for el in payload]
    items = [(el, k, b) for el, k, b in items if b]
    # title
    rule_y = P + TH - rw
    rules = [b for el, k, b in items if el.get('type') == 'line' and b[1] == rule_y and b[0] == P and b[2] == W - P - 1]
    if not rules:
        errs.append(f'title rule not at y={rule_y}')
    texts = [b for el, k, b in items if el.get('type') == 'text' and b[3] < rule_y]
    if texts and min(b[1] for b in texts) != P:
        errs.append(f'title caps start at {min(b[1] for b in texts)}, not P={P}')
    if texts and min(b[0] for b in texts) != P:
        errs.append(f'title starts at x={min(b[0] for b in texts)}, not P={P}')
    stamp = [b for b in texts if b[0] > W // 2]
    if stamp and max(b[2] for b in stamp) != W - 1 - P:
        errs.append(f'update stamp ends at x={max(b[2] for b in stamp)}, not W-P-1={W - 1 - P}')
    # edges: ink stays inside the padding; a fill reaches into it at most S + XS of the text it holds
    # (*Spacing (internal)*, *Chips hang outward*; a hero: of type.data), a warning outline one line.base more (outside the chip's box); a fill with no text stays inside
    from derive_tokens import XS as XS_OF, S as S_OF
    tboxes = [(el, b) for el, k, b in items if el.get('type') == 'text']
    for el, k, b in items:
        if k == 'ink':
            lx = 0
        else:
            inner = [int(t['size']) for t, tb in tboxes if tb[0] >= b[0] and tb[2] <= b[2] and tb[1] >= b[1] and tb[3] <= b[3]]
            sz = max(inner) if inner else None
            # a hero's fill (HERO_CHIP) is padded with type.data's S, so it hangs by type.data's S + XS (S is the tier's data S)
            lx = (S_OF[sz] + XS_OF[sz] if sz in S_OF else S + S // 2) if sz else 0
            if el.get('type') == 'rectangle' and 'fill' not in el and el.get('width', 1) >= 2:
                lx += el['width'] // 2
        if b[0] < P - lx or b[2] > W - 1 - P + lx or b[1] < P - lx or b[3] > H - 1 - P + lx:
            what = (el.get('value') or el.get('type'))
            errs.append(f'{k} {str(what)[:24]!r} at {b} outside padding' + (f' (+ {lx} px for its text)' if lx else ''))
    # gap below the title rule
    below = [(el, b) for el, k, b in items if k == 'ink' and b[1] > rule_y + rw - 1]
    heroes = [(el, b) for el, k, b in items if el.get('type') == 'text' and 'SpaceGrotesk' in str(el.get('font'))]
    if gap_rule in ('M', 'M+') and below:
        el0, b0 = min(below, key=lambda eb: eb[1][1])
        g = b0[1] - (rule_y + rw)
        if 'SpaceGrotesk' in str(el0.get('font')):
            want = int(el0['size']) // HERO_GAP_DIV          # hero clearance: a hero numeral at the top sits size / 7 below the rule
            if g != want:
                errs.append(f'hero starts {g} px below the rule, not size/7={want}')
        elif g != M and not (gap_rule == 'M+' and g > M):
            errs.append(f'content starts {g} px below the rule, not M={M}')
    # 'C': the hero band is centred between the title rule and the next full-width rule (equal gaps, 2 px tolerance, both >= M)
    if gap_rule == 'C':
        lines = sorted(b[1] for el, k, b in items if el.get('type') == 'line' and b[1] > rule_y + rw and b[2] - b[0] > W * 0.6)
        if lines:
            ny = lines[0]
            band = [b for el, k, b in items if k == 'ink' and b[1] > rule_y + rw - 1 and b[3] < ny]
            # a stacked hero group (portrait canvas: the number over its icon) counts the icon at its nominal ink height,
            # the same for every icon of that size (*Hero group*, *Hero centring*): the number keeps its height when the icon changes
            if H > W and heroes:
                from hero_metrics import glyph_height
                hs = max(int(el['size']) for el, _ in heroes)
                nominal = []
                for el, k, b in items:
                    if k == 'ink' and b[1] > rule_y + rw - 1 and b[3] < ny and el.get('type') == 'text' \
                            and 'materialdesign' in str(el.get('font')) and el.get('size', 0) >= hs * 0.4 and el.get('anchor', 'mm') == 'mm':
                        half = glyph_height(int(el['size'])) / 2
                        nominal.append((b, [b[0], round(el['y'] - half), b[2], round(el['y'] + half) - 1]))
                for old, new_b in nominal:
                    band = [new_b if b is old else b for b in band]
            if band:
                gt = min(b[1] for b in band) - (rule_y + rw)
                gb = ny - max(b[3] for b in band) - 1
                if abs(gt - gb) > 2 or min(gt, gb) < M:
                    errs.append(f'hero band not centred: {gt} px above, {gb} px below (M={M})')
    # hero clearance from every full-width rule (above and below)
    rules_h = [b for el, k, b in items if el.get('type') == 'line' and b[1] == b[3] - (int(el.get('width', 1)) - 1) and b[2] - b[0] > W * 0.4]
    if bp in WORD:                # a flagged word fills the hero block (*Glance with a word*, *Flagged*): a fill behind a hero word is that
        from derive_tokens import S as S_ALL                # block, M below the title line and space.s of the title into the padding sideways
        sx = S_ALL[tier_tokens(bp)['type']['title'][1]]
        block = [P - sx, P + TH + M, W - P - 1 + sx, H - P - 1]
        b0 = tier_tokens(bp)['line']['base']
        ring = [block[0] - b0, block[1] - b0, block[2] + b0, block[3] + b0]        # the warning outline, one line.base outside the box
        blocks = [el for el in payload if el.get('type') == 'rectangle' and [el.get('x_start'), el.get('y_start'), el.get('x_end'), el.get('y_end')] in (block, ring)]
        if want_ns.get('EXPECT_BLOCK') is True and not blocks:
            errs.append('no hero block: this case is flagged, so the hero block is the chip')
        if want_ns.get('EXPECT_FILL') and not any(bl.get('fill') == want_ns['EXPECT_FILL'] for bl in blocks):
            errs.append(f"the hero block's fill is not {want_ns['EXPECT_FILL']}: {[bl.get('fill') for bl in blocks]}")
        if want_ns.get('EXPECT_BLOCK') is False and blocks:
            errs.append('a hero block on a case that is not flagged')
        for bl in blocks:          # everything in the block takes the on-colour (*Glance with a word*, *Flagged*)
            on = 'black' if bl.get('fill') in (None, 'yellow') else 'white'
            for el in payload:
                x, y = el.get('x'), el.get('y')
                if el.get('type') in ('text', 'icon') and isinstance(x, (int, float)) and isinstance(y, (int, float)) and y >= P + TH \
                        and bl['x_start'] <= x <= bl['x_end'] and bl['y_start'] <= y <= bl['y_end'] and el.get('color', 'black') != on:
                    errs.append(f"{str(el.get('value'))[:16]!r} in {el.get('color')} on the hero block, not {on}")
            if bl.get('fill') is None:
                inner = bl['x_start'] + int(bl.get('width', 1))
                for hel, hb in heroes:
                    if hb[0] < inner + 1:
                        errs.append(f"the block's outline touches the word {hel['value']!r} (ink from x={hb[0]}, outline to {inner - 1})")
        for hel, hb in heroes:
            behind = [el for el, k, b in items if el.get('type') == 'rectangle' and el.get('fill') != 'white'
                      and el['x_start'] <= hb[0] and el['x_end'] >= hb[2] and el['y_start'] <= hb[1] and el['y_end'] >= hb[3]]
            for el in behind:
                got = [el['x_start'], el['y_start'], el['x_end'], el['y_end']]
                if got not in (block, ring):
                    errs.append(f'a fill behind the hero word at {got}, not the hero block {block}')
            if hel.get('color') != 'black' and not behind:
                errs.append(f"hero word {hel['value']!r} in {hel.get('color')} without the block behind it")
    for el, b in heroes:
        # one word keeps the hero clearance as a numeral does; two stacked words keep M (*Hero group*, hero clearance)
        want = M if (bp in WORD and len(heroes) > 1) else (int(el['size']) // HERO_GAP_DIV)
        for r in rules_h:
            if r[3] < b[1] and b[1] - r[3] - 1 < want:
                errs.append(f'hero {el["value"]!r} only {b[1] - r[3] - 1} px below a rule (min {want})')
            if r[1] > b[3] and r[1] - b[3] - 1 < want:
                errs.append(f'hero {el["value"]!r} only {r[1] - b[3] - 1} px above a rule (min {want})')
    if bp in PROGRESS and heroes:
        # the bar: one track, a hero gap (size / 7) under the hero group's ink, digits and icon (*Glance with a progress bar*, *One block*)
        tr = tracks(payload, tier_tokens(bp)['line']['base'])
        hs = max(int(el['size']) for el, _ in heroes)
        group = [b for el, k, b in items if k == 'ink' and b[1] > rule_y + rw - 1 and (el in [h for h, _ in heroes]
                 or (el.get('type') == 'text' and 'materialdesign' in str(el.get('font')) and el.get('size', 0) >= hs * 0.4))]
        if len(tr) != 1:
            errs.append(f'{len(tr)} progress tracks under the hero, not one')
        elif not bar_top_ok(heroes, tr[0], hs, layout_icon_steps(bp)):
            errs.append(f'the bar starts at y={tr[0][1]}, not a hero gap under the hero group counted with its largest icon (y={bar_top_ok(heroes, tr[0], hs, layout_icon_steps(bp), want=True)})')
        else:
            x0, y0, x1, y1 = tr[0]
            base = tier_tokens(bp)['line']['base']
            inside = [el for el in payload if el.get('type') == 'rectangle' and el.get('fill') and x0 < el['x_start'] and el['x_end'] < x1 and y0 < el['y_start'] and el['y_end'] < y1]
            # flagged, the bar fills in the level's colour (*Glance with a progress bar*, *Flagged*)
            if want_ns.get('EXPECT_FILL') and want_ns['EXPECT_FILL'] not in [el.get('fill') for el in inside]:
                errs.append(f"the bar's fill is not {want_ns['EXPECT_FILL']}: {[el.get('fill') for el in inside]}")
            # filled to the share done (*Glance with a progress bar*, *The bar*)
            if want_ns.get('EXPECT_SHARE') is not None:
                fw = max([el['x_end'] - el['x_start'] + 1 for el in inside if el['y_end'] - el['y_start'] > 1] or [0])
                want = round((x1 - x0 + 1 - 2 * base) * want_ns['EXPECT_SHARE'] / 100)
                if abs(fw - want) > 2:
                    errs.append(f"the bar is filled {fw} px, not {want_ns['EXPECT_SHARE']}% ({want} px)")
            # the Glance secondary a hero gap under the track, measured to its chip box, which holds its text (*Glance with a progress bar*, *One block*)
            # the Glance secondary's chip box a hero gap under the track: proven where the box is drawn, on a flagged case (a chip
            # drawn as an outline sits one line.base outside it)
            want_y = y1 + 1 + hs // HERO_GAP_DIV
            for el in payload:
                if el.get('type') == 'rectangle' and el['y_start'] > y1 and el['x_end'] - el['x_start'] > 40:
                    out = 'fill' not in el and int(el.get('width', 1)) > base
                    if not (abs(el['y_start'] - want_y) <= 1 or (out and want_y - 2 * base - 1 <= el['y_start'] <= want_y)):
                        errs.append(f"the Glance secondary's chip starts at y={el['y_start']}, not a hero gap under the bar (y={want_y})")
            # as wide as the widest reading's digits, a hero gap and the largest hero icon's box, never wider than the content (*Glance with a progress bar*, *The bar*)
            want_w = min(W - 2 * P, hero_ink_w(widest_of(bp), hs) + hs // HERO_GAP_DIV + layout_icon_steps(bp)[0])
            if abs((x1 - x0 + 1) - want_w) > 2 or abs((x0 + x1 + 1) / 2 - W / 2) > 1:
                errs.append(f'the bar is {x1 - x0 + 1} px wide from x={x0}, not {want_w} px centred')
            # the chip at the level: its fill, or the warning outline (*Glance*, *Severity takes the Glance secondary*)
            if want_ns.get('EXPECT_CHIP'):
                chips = [('outline' if 'fill' not in el and int(el.get('width', 1)) > base else el.get('fill')) for el in payload if el.get('type') == 'rectangle'
                         and el['y_start'] > y1 and el['x_end'] - el['x_start'] > 40]
                if want_ns['EXPECT_CHIP'] not in chips:
                    errs.append(f"the Glance secondary's chip is not {want_ns['EXPECT_CHIP']}: {chips}")
    # the footer's line: whatever is above it keeps M clear of it (*Footer*: room)
    fy = H - P - footer_height(bp)
    # (a footer's line runs from padding to padding; a chart's axis on the same row stops short for its labels)
    if [1 for el, k, b in items if el.get('type') == 'line' and b[1] == fy and b[0] <= P and b[2] >= W - P - 1]:
        above = [b[3] for el, k, b in items if k == 'ink' and b[3] < fy]
        if above and fy - max(above) - 1 < M:
            errs.append(f'ink ends {fy - max(above) - 1} px above the footer line (min M={M})')
    if bottom_rule == 'fill':
        bot = max(b[3] for el, k, b in items if k == 'ink')
        if bot != H - P - 1:
            errs.append(f'lowest ink on row {bot}, not H-P-1={H - P - 1}')
    errs += group_checks(payload, items, P)
    errs += c7_checks(payload, items, W, H)
    PAYLOADS[f'{scen}@{bp}'] = (bp, payload, items)
    keep = __import__('os').environ.get('EP_RENDERS')      # keep the render for the reference comparison (baseline.py cmp)
    if keep:
        import json, shutil
        pathlib.Path(keep).mkdir(parents=True, exist_ok=True)
        shutil.copy(CHECK_PNG, f'{keep}/{bp}__{scen}.png')
        pathlib.Path(f'{keep}/{bp}__{scen}.json').write_text(json.dumps(payload, ensure_ascii=False, sort_keys=True))
    return errs


PAYLOADS = {}


def _cross(a, b):
    return a[0] <= b[2] and b[0] <= a[2] and a[1] <= b[3] and b[1] <= a[3]


def _inside(a, b):
    return b[0] <= a[0] and a[2] <= b[2] and b[1] <= a[1] and a[3] <= b[3]


def c7_checks(payload, items, W, H):
    errs = []
    def is_text(e):
        f = str(e.get('font', ''))
        return e.get('type') == 'text' and (f.startswith('TRMNL') or f.startswith('SpaceGrotesk'))
    def is_icon(e):
        return e.get('type') == 'text' and 'materialdesign' in str(e.get('font', ''))
    texts = [(e, b) for e, k, b in items if is_text(e)]
    icons = [(e, b) for e, k, b in items if is_icon(e)]
    lines = [(e, b) for e, k, b in items if e.get('type') == 'line']
    fills = [(e, b) for e, k, b in items if k == 'fill' and e.get('type') == 'rectangle']
    # overlap: text against text, icons and lines
    for i, (e, b) in enumerate(texts):
        for e2, b2 in texts[i + 1:] + icons + lines:
            if _cross(b, b2):
                errs.append(f'overlap: {str(e["value"])[:16]!r} at {b} with {e2.get("type")} {str(e2.get("value", ""))[:16]!r} at {b2}')
    # hero: nothing drawn after a hero numeral covers it
    order = {id(e): n for n, e in enumerate(payload)}
    for e, b in texts:
        if not str(e.get('font', '')).startswith('SpaceGrotesk'):
            continue
        for e2, k2, b2 in items:
            if order.get(id(e2), -1) > order.get(id(e), -1) and _cross(b, b2) and not str(e2.get('font', '')).startswith('SpaceGrotesk'):
                errs.append(f'hero {str(e["value"])!r} covered by {e2.get("type")} {str(e2.get("value", ""))[:12]!r}')
    # chips: on the canvas, text inside its fill
    for e, b in fills:
        if b[0] < 0 or b[1] < 0 or b[2] > W - 1 or b[3] > H - 1:
            errs.append(f'fill at {b} leaves the canvas')
    for e, b in texts:
        for e2, b2 in fills:
            if order.get(id(e2), -1) < order.get(id(e), -1) and _cross(b, b2) and not _inside(b, b2):
                errs.append(f'text {str(e["value"])[:16]!r} at {b} sticks out of its fill at {b2}')
    return errs


def _layouts(test):
    """the layouts (check keys) of the pages in registry.yaml that pass test(page definition, page's pattern)"""
    import pages
    from registry import load
    out = []
    for page, v in load()['pages'].items():
        if v.get('blueprints') and page in pages.names() and test(pages.load(page), v['uses']):
            out += v['blueprints']
    return out


# derived from the registry and the page definitions, never listed
WEATHER = _layouts(lambda d, u: any(i.get('name') == 'pollen_sensor' for i in d.get('inputs') or []))   # layouts with pollen inputs
SAME = _layouts(lambda d, u: u.split('/')[0] in ('glance', 'hero-dashboard', 'bar-chart', 'line-chart', 'timeline'))   # nothing moves between states: a hero, a chart's frame
MODULE = _layouts(lambda d, u: u == 'hero-dashboard/module')   # two halves (design system: Hero dashboard with a chart or list)
DASH = _layouts(lambda d, u: u.split('/')[0] == 'hero-dashboard')
PROGRESS = _layouts(lambda d, u: u == 'glance/progress')   # a bar under the hero (*Glance with a progress bar*)
WORD = _layouts(lambda d, u: u == 'glance/word')   # the hero is a word: its size and place follow the word (*Glance with a word*)
CHART = _layouts(lambda d, u: u.split('/')[0] in ('bar-chart', 'line-chart', 'timeline'))   # the frame stays put: title line, baseline, footer line
ZERO = _layouts(lambda d, u: u == 'bar-chart/prices')   # the baseline is the zero line, so it moves on a day with a negative price (*Bar chart for prices*, Baseline)


def signature(bp, payload):
    hero = sorted({e['size'] for e in payload if e.get('type') == 'text' and str(e.get('font', '')).startswith('SpaceGrotesk')})
    lines = sorted({(e['y_start'], min(e['x_start'], e['x_end']), max(e['x_start'], e['x_end'])) for e in payload
                    if e.get('type') == 'line' and e['y_start'] == e['y_end'] and abs(e['x_end'] - e['x_start']) > 40
                    and not e.get('dashed') and e.get('fill') != 'white'})
    # chips: filled, or outlined where the panel has no warning colour (a stroke of 2 × line.base, no fill)
    fills = [(e['y_start'], e['x_start'], e['x_end'], e['y_end']) for e in payload if e.get('type') == 'rectangle'
             and (e.get('fill') not in (None, 'white') or ('fill' not in e and e.get('width', 1) >= 2))
             and abs(e['x_end'] - e['x_start']) > 100]
    if bp in CHART:               # a chart's frame lines run the plot's width; shorter ones are its data (flat runs of a series)
        lines = [l for l in lines if l[2] - l[1] >= 0.6 * SIZES[bp][0]]
        if bp in ZERO:            # its baseline is left out: the title line and the footer's line (in the canvas's last fifth) stay
            lines = [l for i, l in enumerate(lines) if i == 0 or l[0] > 0.8 * SIZES[bp][1]]
    sig = {'hero size': hero, 'lines': lines, '_fills': fills}
    if bp in PROGRESS:            # the bar doesn't change with the time shown, the state or the level (*Glance with a progress bar*, The bar; One block)
        sig['bar'] = tracks(payload, tier_tokens(bp)['line']['base'])
    if bp in DASH and hero:
        sig['hero icon'] = sorted({e['size'] for e in payload if e.get('type') == 'text' and 'materialdesign' in str(e.get('font', ''))
                                   and e.get('size', 0) >= hero[-1] * 0.4})
    return sig


def hero_ink_w(t, hs):
    """a hero reading's ink width (the kit measures it from advances and side bearings, HERO_INK_W: up to 2 px apart from
    the drawn ink, which is kerned)"""
    b = ImageFont.truetype(str(ROOT / 'fonts' / 'SpaceGrotesk-Bold.ttf'), hs).getmask(t).getbbox()
    return b[2] - b[0]


def widest_of(bp):
    """the page's widest reading (registry.yaml)"""
    from registry import load
    return next(str(v.get('widest')) for v in load()['pages'].values() if bp in (v.get('blueprints') or []))


def layout_icon_steps(bp):
    """the layout's icon.heroAloneSteps (EP_LAYOUT in the tokens of the package being checked)"""
    import re
    path = pathlib.Path(os.environ.get('EP_CT') or ROOT / 'lib') / 'ep_tokens.jinja'
    m = re.search(r"'%s': \{.*?'heroAloneSteps': \[([0-9, ]+)\]" % re.escape(bp), path.read_text(), re.S)
    return [int(x) for x in m.group(1).split(',')]


def bar_top_ok(heroes, track, hs, steps, want=False):
    """the track a hero gap under the hero group, its icon counted at the largest hero icon's nominal ink height (HERO_BLOCK_Y)"""
    from hero_metrics import glyph_height, measure
    el = max((e for e, _ in heroes), key=lambda e: int(e['size']))
    _, up, dn, _ = measure(hs)
    y = round(int(el['y']) + max(dn, glyph_height(steps[0]) / 2) + hs // HERO_GAP_DIV)
    return y if want else abs(track[1] - y) <= 1


def tracks(payload, base):
    """a progress bar's tracks: ink outlines of line.base without a fill, wider than high (a warning outline is 2 x line.base)"""
    return sorted((e['x_start'], e['y_start'], e['x_end'], e['y_end']) for e in payload if e.get('type') == 'rectangle' and 'fill' not in e
                  and e.get('outline') == 'black' and int(e.get('width', 1)) == base and e['x_end'] - e['x_start'] > 4 * (e['y_end'] - e['y_start']))


def pollen_off(scen):
    """the scenario shows no pollen: no pollen sensor, or its type (or the sensor) at 0"""
    import os
    os.environ.setdefault('EP_ROOT', str(ROOT))
    ns = {}
    try:
        exec((ROOT / 'scen' / f'{scen}.py').read_text(), ns)
    except Exception:
        return False
    inp, st = ns.get('INPUTS') or {}, ns.get('STATES') or {}
    ps = inp.get('pollen_sensor')
    if not ps or ps not in st:
        return True
    pt = inp.get('pollen_type')
    det = [d.get('value') for d in (st[ps].get('attributes') or {}).get('details') or [] if pt and d.get('name') == pt]
    return (det[0] if det else float(st[ps].get('state') or 0)) in (0, '0')


def scen_flag(scen, name):
    """a scenario's own setting"""
    import os
    os.environ.setdefault('EP_ROOT', str(ROOT))
    ns = {}
    try:
        exec((ROOT / 'scen' / f'{scen}.py').read_text(), ns)
    except Exception:
        return None
    return ns.get(name)


def scen_lang(scen):
    """the language a scenario draws in"""
    import os
    os.environ.setdefault('EP_ROOT', str(ROOT))
    ns = {}
    try:
        exec((ROOT / 'scen' / f'{scen}.py').read_text(), ns)
    except Exception:
        return ''
    return (ns.get('INPUTS') or {}).get('weekday_format', 'en')


def same_layout():
    errs = []
    for bp in SAME:
        # states compared: not the error view, and not pollen at 0 or without a pollen sensor (the pollen row makes way)
        sc = [(s, signature(b, p)) for s, (b, p, _) in PAYLOADS.items() if b == bp and 'err' not in s and s.split('@')[0] not in CONFIG_CASES
              and not (bp in WEATHER and pollen_off(s.split('@')[0]))]
        if bp in PROGRESS:        # not running and the error state have no hero block to keep in place (*Appliance run*); the cases say which
            for s, sig in sc:
                if not sig['hero size'] and not scen_flag(s.split('@')[0], 'NO_BLOCK'):
                    errs.append(f'{bp}: {s} has no hero block, and is no case without one')
            sc = [(s, sig) for s, sig in sc if not scen_flag(s.split('@')[0], 'NO_BLOCK')]
        if bp in MODULE:          # a Hero dashboard with a module: the hero band and the divider stay put; the module's own lines follow its data
            (P, TH, M, rw), _ = tier_vals(bp)
            ym = (P + TH + SIZES[bp][1] - P) // 2
            sc = [(s, dict(sig, lines=[l for l in sig['lines'] if l[0] <= ym])) for s, sig in sc]
        # the hero stays at its height in every state, pollen at 0 included: what appears takes a place that was kept for it
        ys = {}
        for s, (b, p, _) in PAYLOADS.items():
            if b == bp and bp not in WORD and 'err' not in s and s.split('@')[0] not in CONFIG_CASES:
                h = [e['y'] for e in p if e.get('type') == 'text' and 'SpaceGrotesk' in str(e.get('font', ''))]
                if h:
                    ys.setdefault(h[0], []).append(s.split('@')[0])
        if bp in WORD:            # the size follows the word, so cases are compared per word: nothing moves when a chip appears
            per = {}
            for s, (b, p, _) in PAYLOADS.items():
                if b == bp and 'err' not in s:
                    hh = [(e['value'], e['size'], e['x'], e['y']) for e in p if e.get('type') == 'text' and 'SpaceGrotesk' in str(e.get('font', ''))]
                    icons = tuple((e['size'], e['x']) for e in p if (e.get('type') == 'text' and 'materialdesign' in str(e.get('font', '')) or e.get('type') == 'icon') and e.get('size', 0) >= 24)
                    if hh:          # the word, where it is, and its icon: nothing moves or changes size when a chip appears
                        per.setdefault(tuple(v for v, _, _, _ in hh), {}).setdefault(tuple((z, x, y) for _, z, x, y in hh) + icons, []).append(s.split('@')[0])
            for words, places in per.items():
                if len(places) > 1:
                    errs.append(f'{B[bp]}: the hero {" / ".join(words)} moves between states: ' + '; '.join(f'{k} in {", ".join(v[:4])}' for k, v in places.items()))
        if len(ys) > 1:
            most = max(ys, key=lambda y: len(ys[y]))
            errs.append(f'{B[bp]}: the hero moves between states: at y={most} in {len(ys[most])} cases, but ' +
                        '; '.join(f'y={y} in {", ".join(v[:4])}' for y, v in sorted(ys.items()) if y != most))
        if len(sc) < 2:
            continue
        if bp in CHART:           # a chart's label margin follows the language (the decimal separator's width), so states are
            lang = {}             # compared within one language; the first case's language is the one compared
            for s, sig in sc:
                lang.setdefault(scen_lang(s.split('@')[0]), []).append((s, sig))
            sc = max(lang.values(), key=len)
            if len(sc) < 2:
                continue
        ref_s, ref = sc[0]
        def replaced(y, x0, x1, fills):
            # a chip that takes a line's place (the footer's, the pollen row's) keeps the layout: a full-width chip just below
            # the line, or one that covers it (touching warning outlines merge into one, OMERGE)
            return any(((fy >= y and fy - y <= 10) or fy <= y <= fye) and fx0 <= x0 + 10 and fx1 >= x1 - 10 for fy, fx0, fx1, fye in fills)
        for s, sig in sc[1:]:
            for k in ref:
                if k.startswith('_'):
                    continue
                if k == 'lines':
                    a, b = set(sig[k]), set(ref[k])
                    odd = [l for l in a - b if not replaced(*l, ref['_fills'])] + [l for l in b - a if not replaced(*l, sig['_fills'])]
                    if odd:
                        errs.append(f'{bp}: lines in {s} differ from {ref_s}: {sorted(odd)}')
                elif k == 'hero size' and bp in WORD:
                    continue
                elif sig.get(k) != ref[k]:
                    errs.append(f'{bp}: {k} in {s} differs from {ref_s}: {sig.get(k)} vs {ref[k]}')
    return errs


def group_checks(payload, items, L):
    """hero group vs text: >= space.l sideways where they share rows; the badge's paper ring never cuts a rule"""
    errs = []
    hero = [(e, b) for e, k, b in items if b and e.get('type') == 'text' and e.get('font') == 'SpaceGrotesk-Bold.ttf']
    if not hero:
        return errs
    hs = max(e['size'] for e, _ in hero)
    grp = [b for _, b in hero] + [b for e, k, b in items if b and e.get('type') == 'text' and 'materialdesign' in str(e.get('font')) and e.get('size', 0) >= hs * 0.4]
    circ = [e for e in payload if e.get('type') == 'circle']
    grp += [[c['x'] - c['radius'], c['y'] - c['radius'], c['x'] + c['radius'], c['y'] + c['radius']] for c in circ]
    for e, k, b in items:
        if not b or e.get('type') != 'text' or not str(e.get('font', '')).startswith('TRMNL'):
            continue
        if 'Regular' in str(e.get('font')) and any(abs(b[3] - hb[3]) <= 1 and 0 <= b[0] - hb[2] <= L for _, hb in hero):
            continue          # the hero's unit
        for h in grp:
            if b[1] <= h[3] and h[1] <= b[3]:
                gap = max(b[0] - h[2], h[0] - b[2]) - 1
                if gap < L:
                    errs.append(f'{str(e["value"])[:14]!r} only {gap} px from the hero group (space.l {L})')
    rules = []
    for e in payload:
        if e.get('type') == 'line' and e['y_start'] == e['y_end'] and abs(e['x_end'] - e['x_start']) > 40:
            rules.append((min(e['x_start'], e['x_end']), e['y_start'], max(e['x_start'], e['x_end']), e['y_start'] + e.get('width', 1) - 1))
        if e.get('type') == 'rectangle' and abs(e['y_end'] - e['y_start']) <= 3 and abs(e['x_end'] - e['x_start']) > 40 and e.get('fill') not in (None, 'white'):
            rules.append((e['x_start'], e['y_start'], e['x_end'], e['y_end']))
    for c in circ:
        r = c['radius']
        for x0, y0, x1, y1 in rules:
            if c['x'] + r >= x0 and c['x'] - r <= x1 and c['y'] + r >= y0 and c['y'] - r <= y1:
                errs.append(f'moon badge ring cuts the rule at y={y0}')
    return errs


# ---- running many cases: in parallel, one process per core; results in the cases' order ----
_POOL = None


def _one(a):
    out, scen, bp, g, bt, sized = a
    try:
        errs = check(out, scen, bp, g, bt, sized)
    except SystemExit as ex:
        errs = [f'render failed: {ex}']
    except Exception as ex:                # a candidate a layout can't draw (a size its tables don't cover) fails, it doesn't crash
        errs = [f'render failed: {type(ex).__name__}: {ex}']
    key = f'{scen}@{bp}'
    return errs, key, PAYLOADS.get(key)


def only_keys():
    """the layouts EP_KEYS names (comma-separated layout keys); a key that is no layout stops the run, so a typing error
    can't pass as '0 cases'"""
    only = [k for k in os.environ.get('EP_KEYS', '').split(',') if k]
    unknown = [k for k in only if k not in B]
    if unknown:
        sys.exit(f'EP_KEYS: no layout {", ".join(unknown)} (layouts: {", ".join(sorted(B))})')
    return only


def jobs():
    """how many cases run at once: EP_JOBS when set (a laptop in use, a small CI runner), else one per core"""
    import os
    return max(1, int(os.environ.get('EP_JOBS') or os.cpu_count() or 1))


def run_cases(out, cases):
    """check every (scenario, blueprint, gap rule, bottom rule, sized) case of the package at out; returns each case's errors,
    in order, and keeps the payloads for same_layout. EP_CT (and EP_RENDERS) must be set before the first call."""
    global _POOL
    import multiprocessing
    if _POOL is None:
        _POOL = multiprocessing.get_context('spawn').Pool(jobs())
    res = _POOL.map(_one, [(out,) + tuple(c) for c in cases], chunksize=1)
    for _, key, pl in res:
        if pl is not None:
            PAYLOADS[key] = pl
    return [r[0] for r in res]


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit('usage: check.py PKG   (a built package; set EP_CT to its custom_templates)')
    out = sys.argv[1]
    bad = 0
    ALL = [c + (False,) for c in CASES] + [c + (True,) for c in EXTRA_CASES]
    for e in universal_selftest(CASES[0][1]):
        print('SELFTEST', e); bad += 1
    only = only_keys()                      # check a few layouts while building
    if only:
        ALL = [c for c in ALL if c[1] in only]
    for (scen, bp, g, bt, sized), errs in zip(ALL, run_cases(out, ALL)):
        bad += bool(errs)
        print(('FAIL ' if errs else 'ok   ') + f'{scen:12s} {B[bp]}' + (' (weather extra)' if sized else ''))
        for e in errs:
            print('       - ' + e)
    se = same_layout()
    for e in se:
        print('SAME ' + e)
    print(f'\n{len(ALL) - bad}/{len(ALL)} cases pass' + (f'; {len(se)} layout differences between states' if se else ''))
    sys.exit(1 if bad or se else 0)
