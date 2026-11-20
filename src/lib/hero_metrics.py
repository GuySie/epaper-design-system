#!/usr/bin/env python3
"""Generate the hero ladder and its measured Space Grotesk Bold tables (design system: Hero sizes).

The ladder is a rule, not a list of picks: multiples of 8 from 56 to 160 (steps of 5-14 %), then multiples of 32
up to 320 for the dense large screens. For every rung this measures, in Pillow's 1-bit rendering (as drawcustom draws):
  SGB  the left side bearing of each character at anchor 'lm' (ink starts this far right of x)
  SGR  the right side bearing of each character (the advance ends this far right of the ink)
  HUP  the digits' ink above the anchor line (the tallest digit)
  HDN  the digits' ink below the anchor line (the lowest digit)
  HWR  each character's advance as a share of the size (size-independent)
  ICH  the median weather glyph height of every icon rung (see below)
  ICB  each MDI glyph's blank margin inside its box, left, right, top and bottom, as a share of the size (centring by ink)
With them a string's ink width is its advance (HWR) less the first character's SGB and the last one's SGR.

Icons follow the hero (design system: Hero group). The icon ladder is 16, 20, 24, then multiples of 8 to 160, then
multiples of 32 to 320. An icon's glyph height is the median ink of the weather glyphs the blueprints draw (measured),
so for a hero size h with digit ink D:
  Grid icon       the largest rung whose glyph height is <= D
  Glance steps    every rung from the largest whose glyph height is <= 1.2 x D down to the smallest whose glyph
                  height is >= 2/3 x D (below it the icon drops out)

usage: hero_metrics.py            print the three tables as Jinja sets
       hero_metrics.py --write    replace them in ds_macros.jinja
       hero_metrics.py --pairs    print the Grid icon and the Glance steps for every hero size
"""
import json, pathlib, re, statistics, sys
from PIL import ImageFont

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from derive_tokens import HERO_SIZES as HERO_LADDER, ICON_LADDER     # noqa: E402  the ladders' one home
# the digits and their signs, and for a word as the hero (*Glance with a word*) the capitals of the eight languages
CHARS = '-0123456789°.,:%' + ' +&/ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜÅÉÈÊËÁÀÂÍÓÚÑÇŁŚŻŹĆĘĄŃČŠŽĐÎÔÛÙÏŒÆØÒÌÝ—!?()' + "'"
WEATHER = ['weather-night', 'weather-cloudy', 'weather-fog', 'weather-hail', 'weather-lightning', 'weather-lightning-rainy',
           'weather-partly-cloudy', 'weather-pouring', 'weather-rainy', 'weather-snowy', 'weather-snowy-rainy', 'weather-sunny',
           'weather-windy', 'weather-windy-variant', 'alert-circle-outline', 'weather-night-partly-cloudy']


def glyph_height(s):
    """median ink height of the weather glyphs at icon size s"""
    mdi = json.load(open(ROOT / 'mdi_map.json'))
    f = ImageFont.truetype(str(ROOT / 'fonts' / 'materialdesignicons-webfont.ttf'), s)
    hs = []
    for n in WEATHER:
        m, off = f.getmask2(mdi[n], mode='1', anchor='mm'); b = m.getbbox(); hs.append(b[3] - b[1])
    return int(statistics.median(hs))


def pairs():
    g = {s: glyph_height(s) for s in ICON_LADDER}
    out = {}
    for h in HERO_LADDER:
        _, up, dn, _ = measure(h); d = up + dn + 1
        from derive_tokens import HERO_ICON_K, HERO_ICON_K_ALONE, HERO_ICON_MIN     # the Hero group rule's constants
        grid = max((s for s in ICON_LADDER if g[s] <= HERO_ICON_K * d), default=None)
        top = max((s for s in ICON_LADDER if g[s] <= HERO_ICON_K_ALONE * d), default=None)
        low = min(s for s in ICON_LADDER if HERO_ICON_MIN[1] * g[s] >= HERO_ICON_MIN[0] * d)
        out[h] = (d, grid, [s for s in sorted(ICON_LADDER, reverse=True) if low <= s <= top])
    return out


def measure(s):
    f = ImageFont.truetype(str(ROOT / 'fonts' / 'SpaceGrotesk-Bold.ttf'), s)
    sgb, sgr, up, dn = {}, {}, [], []
    for c in CHARS:
        m, off = f.getmask2(c, mode='1', anchor='lm')
        x0, y0, x1, y1 = m.getbbox() or (0, 0, 0, 0)      # a space has no ink
        sgb[c] = off[0] + x0
        sgr[c] = round(f.getlength(c) - (off[0] + x1))
        if c.isdigit():
            up.append(-(off[1] + y0)); dn.append(off[1] + y1 - 1)
    return sgb, max(up), max(dn), sgr


def icon_bearings():
    """left / right / top / bottom blank margin of every glyph in the kit's MDI table, as a share of the icon size (measured
    at 240, anchor 'mm')"""
    src = (ROOT / 'ds_macros.jinja').read_text()
    mdi = eval(re.search(r"\{%- set MDI = (\{.*?\}) -%\}", src, re.S).group(1))
    f = ImageFont.truetype(str(ROOT / 'fonts' / 'materialdesignicons-webfont.ttf'), 240)
    out = {}
    for k, ch in mdi.items():
        m, off = f.getmask2(ch, mode='1', anchor='mm'); b = m.getbbox()
        out[k] = (round((off[0] + b[0] + 120) / 240, 3), round((120 - (off[0] + b[2])) / 240, 3),
                  round((off[1] + b[1] + 120) / 240, 3), round((120 - (off[1] + b[3])) / 240, 3))
    return out


def ratios():
    f = ImageFont.truetype(str(ROOT / 'fonts' / 'SpaceGrotesk-Bold.ttf'), 1000)
    return {c: round(f.getlength(c) / 1000, 4) for c in CHARS}


def reach():
    """({char: ink above the anchor line}, {char: ink below it}), as shares of the size: an accent rises above the
    digits and a tail (Q, Ç) hangs below them, and a hero chip around a word covers both"""
    f = ImageFont.truetype(str(ROOT / 'fonts' / 'SpaceGrotesk-Bold.ttf'), 1000)
    up, dn = {}, {}
    for c in CHARS:
        m, off = f.getmask2(c, mode='1', anchor='lm')
        b = m.getbbox()
        if b and not c.isdigit():
            up[c] = round(-(off[1] + b[1]) / 1000, 3); dn[c] = round((off[1] + b[3] - 1) / 1000, 3)
    return up, dn


def tables():
    m = {s: measure(s) for s in HERO_LADDER}
    g = {s: glyph_height(s) for s in ICON_LADDER}
    dic = lambda i: '{' + ', '.join(f'{s}:{{' + ','.join(f"{c!r}:{m[s][i][c]}" for c in CHARS) + '}' for s in HERO_LADDER) + '}'
    hup = '{' + ', '.join(f'{s}: {m[s][1]}' for s in HERO_LADDER) + '}'
    hdn = '{' + ', '.join(f'{s}: {m[s][2]}' for s in HERO_LADDER) + '}'
    hwr = '{' + ', '.join(f"{c!r}: {v}" for c, v in ratios().items()) + '}'
    up, dn = reach()
    hur = '{' + ', '.join(f"{c!r}: {v}" for c, v in up.items()) + '}'
    hdr = '{' + ', '.join(f"{c!r}: {v}" for c, v in dn.items()) + '}'
    ich = '{' + ', '.join(f'{s}: {g[s]}' for s in ICON_LADDER) + '}'
    icb = '{' + ', '.join(f"'{k}': [{', '.join(str(x) for x in v)}]" for k, v in icon_bearings().items()) + '}'
    return ("{#- generated by lib/hero_metrics.py --write: don't edit by hand -#}\n"
            f"{{%- set HUP = {hup} -%}}\n{{%- set HDN = {hdn} -%}}\n{{%- set SGB = {dic(0)} -%}}\n{{%- set SGR = {dic(3)} -%}}\n"
            f"{{%- set HWR = {hwr} -%}}\n{{%- set HUR = {hur} -%}}\n{{%- set HDR = {hdr} -%}}\n{{%- set ICH = {ich} -%}}\n{{%- set ICB = {icb} -%}}\n{{#- end of generated tables -#}}")

if __name__ == '__main__':
    if '--pairs' in sys.argv:
        for h, (d, grid, steps) in pairs().items():
            print(f'hero {h:3d}  digits {d:3d}  Grid icon {grid}  Glance steps {steps}')
        sys.exit()
    t = tables()
    if '--write' in sys.argv:
        p = ROOT / 'ds_macros.jinja'; src = p.read_text()
        pat = (r"\{#- generated by lib/hero_metrics\.py.*?\{#- end of generated tables -#\}" if 'end of generated tables' in src else
               r"\{%- set HUP = \{.*?\} -%\}\n\{%- set HDN = \{.*?\} -%\}\n\{%- set SGB = \{.*?\}\} -%\}")
        new, n = re.subn(pat, lambda _: t, src, flags=re.S)
        assert n == 1, n
        p.write_text(new); print('ds_macros.jinja: hero tables for', HERO_LADDER)
    else:
        print(t)
