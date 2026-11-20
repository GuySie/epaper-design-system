"""The measured tokens, fitted in the build (design system: Hero group, Hero dashboard, Strip).

Nothing is decided at redraw and nothing is picked by hand: each measured token is the largest value for which the
layout passes the pixel check (check.py), rendered from a built package with the candidate written into its
tokens. Per layout, in this order (the Hero dashboard's what-gives-way order: the hero only steps down when nothing else
can give way):
  1. type.heroShared   the hero beside other content: the largest hero rung for which the layout passes
                       with its widest readings (FIT) (-12° with the moon badge; the event hero at 20:00), the strip icons at
                       their smallest (no hour icon, the day icon at icon.min). icon.heroShared follows by the Hero group rule (lib/hero_metrics.py pairs).
  2. icon.stripHour, icon.stripDay   the strip icons: the hour icon one ladder step below the day icon, the pair as large
                       as passes every check case of the layout (the weather extras included) with that hero; when no pair passes, the hour
                       icon drops out and the day icon is as large as passes. Never below icon.min.
  3. type.heroAlone    the hero on its own (the Glance): the largest hero rung for which the layout
                       passes with its ordinary readings (GLANCE) and keeps its icon; never below the floor (digits >= 7.5 mm).
                       icon.heroAloneSteps follows by the Hero group rule.
A layout without the element has none for the token. lib/gen_tokens.py runs the fits and writes the tokens; it fits a
layout again only when something its fit reads has changed (gen_tokens.layout_hash).
"""
import contextlib, io, os, pathlib, re, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import check                                                  # noqa: E402  the pixel check: the definition of "fits"
from hero_metrics import pairs, HERO_LADDER, ICON_LADDER      # noqa: E402

# layout -> its widest readings (scenario, gap rule): the hero beside other content is the largest rung at which they pass.
# A layout with a hero beside other content is listed here; its strip icons and every other layout are not affected by it
FIT = {
    'weather_27l': [('wxp29h_negmoon', 'C'), ('wxp29h_neg', 'C'), ('wxp29h_plong', 'C')],
    'weather_27p': [('wxp29v_neg', 'C'), ('wxp29v_moon', 'C'), ('wxp29v_plong', 'C')],
    'weather_35': [('wxneg', 'C'), ('wx_moon', 'C'), ('wx_plong', 'C')],
    'weather_41': [('wx42_neg', 'C'), ('wx42_plong', 'C')],
    'weather_75': [('wx75_negmoon', 'C'), ('wx75neg', 'C'), ('wx75_plong', 'C')],
    'weather_75p': [('wx75p_negmoon', 'C'), ('wx75p_neg', 'C'), ('wx75p_plong', 'C')],
    'weather_426': [('w426_negmoon', 'C'), ('w426neg', 'C'), ('w426_plong', 'C')],
    'weather_calendar_75p': [('wxag_widest', 'C')],
    # Value with details: the widest number (-12.5 °C, flagged) and a four-digit one at severe, both with an icon
    'value_details_41': [('vd_widest', 'C'), ('vd_sev', 'C')],
    'value_details_75': [('vd_widest', 'C'), ('vd_sev', 'C')],
    'value_details_75p': [('vd_widest', 'C'), ('vd_sev', 'C')],
    # the event hero: one event, one in progress, and the widest clock time (20:00)
    'appointment_35': [('a35_1', 'M'), ('a35_1now', 'M'), ('a35_1w', 'M')],
    'appointment_41': [('a41_1', 'M'), ('a41_1now', 'M'), ('a41_1w', 'M')],
    'appointment_426': [('a426_1', 'M'), ('a426_1now', 'M'), ('a426_1w', 'M')],
}
# the layouts with forecast strips: every check case of the layout must pass with its strip icons
STRIP = ['weather_41', 'weather_75', 'weather_75p', 'weather_426']
# layout -> its ordinary readings (scenarios; a one-digit count is every digit the cases have): the hero on its own is the
# largest rung at which they pass and keep their icon
GLANCE = {'bin_day_27l': ['bd'], 'bin_day_35': ['bd'], 'bin_day_41': ['bd'], 'weather_glance_14': ['wxp16'], 'doors_windows_14': ['openings_0', 'openings_1', 'openings_2en', 'openings_3'], 'medication_27l': ['med29'], 'weather_glance_35': ['wx35'],
          # Single value: a reading with an icon (a short one on the 1.4", where the unit has the line below)
          'single_value_14': ['sv_wide4'], 'single_value_27l': ['sv_icon'], 'single_value_35': ['sv_icon']}
# of those, the layouts whose hero is fitted on its widest reading instead: the largest rung at which that reading is
# drawn (the layout has one size for every reading), whatever the Glance floor says. The 1.4" Single value: four digits
WIDEST_HERO = {'single_value_14'}

PAIRS = pairs()


def tier_block(src, key):
    i = src.index(f"  '{key}': {{")
    j = src.index("\n  '", i + 5) if "\n  '" in src[i + 5:] else len(src)
    return i, j


def with_tokens(src, key, **kv):
    """src with tokens of one block replaced (a layout's in EP_LAYOUT): type_heroShared=152, icon_stripDay=None, ..."""
    i, j = tier_block(src, key)
    b = src[i:j]
    for name, v in kv.items():
        sect, tok = name.split('_', 1)
        lit = 'none' if v is None else str(v)
        b, n = re.subn(rf"('{sect}': \{{[^}}]*?'{tok}': )(none|\d+|\[[^\]]*\])", lambda m: m.group(1) + lit, b, count=1, flags=re.S)
        assert n == 1, (key, name)
    return src[:i] + b + src[j:]


def passes(pkg, cases, icon_of=None, hero_of=None):
    """'' when every case passes the check, else the first failure. icon_of: the hero size whose icon must be drawn;
    hero_of: the hero size the number must be drawn at."""
    os.environ['EP_CT'] = f'{pkg}/custom_templates'
    # one case at a time: a failing candidate stops at its first failing case, and a try costs about one render either way,
    # so rendering a try's few cases in parallel saves nothing (measured)
    for c in cases:
        with contextlib.redirect_stdout(io.StringIO()):
            try:
                errs = check.check(pkg, *c)
            except SystemExit as e:
                errs = [str(e)]
            except Exception as e:          # a candidate the layout can't draw (a size its tables don't cover) doesn't fit
                errs = [f'render failed: {type(e).__name__}: {e}']
        why = first_failure([c], [errs], icon_of, hero_of)
        if why:
            return why
    return ''


def first_failure(cases, results, icon_of, hero_of=None):
    for (scen, bp, *_), errs in zip(cases, results):
        if not errs and hero_of:
            _, payload, _ = check.PAYLOADS[f'{scen}@{bp}']
            if not [e for e in payload if e.get('type') == 'text' and 'SpaceGrotesk' in str(e.get('font')) and e.get('size') == hero_of]:
                errs = ['the number does not fit']
        if not errs and icon_of:
            _, payload, _ = check.PAYLOADS[f'{scen}@{bp}']
            if not [e for e in payload if ((e.get('type') == 'text' and 'materialdesign' in str(e.get('font'))) or e.get('type') == 'icon') and e.get('size', 0) >= icon_of * 0.4]:
                errs = ['the icon drops out']
        if errs:
            return f'{scen}: {errs[0]}'
    return ''


class Fitter:
    """Fits one package's tokens in place (its custom_templates/ep_tokens.jinja)."""

    def __init__(self, pkg, top=320):
        self.pkg = str(pkg)
        self.path = pathlib.Path(pkg) / 'custom_templates' / 'ep_tokens.jinja'
        self.top = top
        self.log = []

    def _try(self, key, cases, icon_of=None, hero_of=None, **kv):
        src = self.path.read_text()
        self.path.write_text(with_tokens(src, key, **kv))
        why = passes(self.pkg, cases, icon_of, hero_of)
        if why:
            self.path.write_text(src)
        return why

    def hero_shared(self, name, key):
        """type.heroShared of one layout (name: its block in EP_LAYOUT, key: its check cases)"""
        cases = [(s, key, g, 'free') for s, g in FIT[key]]
        why = ''
        for h in sorted((h for h in HERO_LADDER if h <= self.top), reverse=True):
            w = self._try(name, cases, type_heroShared=h, icon_heroShared=PAIRS[h][1])
            if not w:
                self.log.append(f'{key:22s} type.heroShared {h}  (next rung up fails on {why or "nothing: the top rung"})')
                return h
            why = f'{h}: {w}'
        raise SystemExit(f'{key}: no hero rung fits ({why})')

    def strips(self, name, key, imin):
        # every check case of the layout, the weather extras the release also runs on it included
        cases = [c[:4] for c in check.CASES if c[1] == key] + [c[:4] + (True,) for c in check.EXTRA_CASES if c[1] == key]
        rungs = [s for s in ICON_LADDER if s >= imin]
        why = ''
        for i in range(len(rungs) - 1, 0, -1):
            w = self._try(name, cases, icon_stripHour=rungs[i - 1], icon_stripDay=rungs[i])
            if not w:
                self.log.append(f'{key:22s} icon.stripHour {rungs[i - 1]}, icon.stripDay {rungs[i]}  (next pair up fails on {why})')
                return rungs[i - 1], rungs[i]
            why = f'{rungs[i - 1]}/{rungs[i]}: {w}'
        for d in reversed(rungs):
            w = self._try(name, cases, icon_stripHour=None, icon_stripDay=d)
            if not w:
                self.log.append(f'{key:22s} icon.stripHour none, icon.stripDay {d}  (no hour/day pair passes: {why})')
                return None, d
        raise SystemExit(f'{key}: no strip icons fit ({why})')

    def hero_alone(self, name, key, floor):
        cases = [c[:4] for c in check.CASES if c[1] == key and c[0] in GLANCE[key]]
        why = ''
        widest = key in WIDEST_HERO
        if widest:
            floor = min(HERO_LADDER)
        for h in sorted((h for h in HERO_LADDER if floor <= h <= self.top), reverse=True):
            w = self._try(name, cases, icon_of=None if widest else h, hero_of=h if widest else None, type_heroAlone=h, icon_heroAloneSteps=PAIRS[h][2])
            if not w:
                self.log.append(f'{key:22s} type.heroAlone {h}  (next rung up fails on {why or "nothing: the top rung"})')
                return h
            why = f'{h}: {w}'
        raise SystemExit(f'{key}: no Glance hero at or above the floor {floor} fits ({why})')
