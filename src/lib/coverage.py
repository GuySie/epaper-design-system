#!/usr/bin/env python3
"""Case coverage: every layout names a check case for every kind of state it must be tested in (CLAUDE.md, *How a change goes*, step 7).

  coverage.py        lint: every layout (pixcmp_cases.B) has every kind, each a check case of that layout (or a weather extra
                     for the layouts baseline.py renders them on), 'n/a: <why>', or 'GAP'. A missing kind, an unknown or
                     foreign scenario fails; GAPs are listed on every run until a case fills them.
A new layout is added here with its cases; a new kind of state is added to KINDS / WX_KINDS.
"""
import pathlib, sys
LIB = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(LIB))
from pixcmp_cases import B, CASES, WEATHER_EXTRA, EXTRA_KEYS      # noqa: E402

KINDS = ['normal', 'widest', 'warning', 'severe', 'gray', 'colour', 'title', 'stale', 'error', 'unavailable', 'empty']
WX_KINDS = KINDS + ['alert', 'pollen 0', 'pollen widest']


def wx(normal, widest, warning, severe, gray, colour, title, stale, error, alert, p0, pw, unav='wx_unav', empty=None):
    return dict(zip(WX_KINDS, (normal, widest, warning, severe, gray, colour, title, stale, error, unav, empty or NOLIST, alert, p0, pw)))


def pg(normal, widest, warning, severe, gray, colour, title, stale, error, unav, empty):
    return dict(zip(KINDS, (normal, widest, warning, severe, gray, colour, title, stale, error, unav, empty)))


NOTHR = 'n/a: the page has no thresholds (*Thresholds*)'
NOWARN = 'n/a: the page has no warning level, only severe (*Thresholds*)'
NOCHIP = 'n/a: no thresholds, so no warning or severe chips to show on a panel'
NOSTALE = 'n/a: the page has no stale state (*Title row*, stale chip)'
NOERR = 'n/a: the page has no error view'
MONO = 'n/a: the 4.26" kit has no colour panel'
NOERRV = 'n/a: the page has no error view (its sensor is required; an unavailable one draws a dash)'
NOLIST = 'n/a: the page has no list or chart that can be empty (pollen at 0 is its own kind)'
NOEMPTY = 'n/a: the page has no list or chart that can be empty'
REQ = 'n/a: the first entry is required, so the list is never empty'
NOHIST = 'n/a: a chart without history is the error view'
EVENTS = 'n/a: an event has no value that can be unavailable; an unavailable calendar is the error view'
COVERAGE = {
    # weather (an official orange alert is the severe case: it draws the severe chip)
    'weather_glance_14':     wx('wxp16', 'wxp16_negmoon', 'wxp16_warn', 'wxp16_alert', 'wxp16_warn_g', 'wxp16_y', 'wxp16_title', 'wx_stale', 'wx_err', 'wxp16_alert', 'wx_p0', 'wxp16_plong'),
    'weather_27l':    wx('wxp29h', 'wxp29h_negmoon', 'wx_warn', 'wxp29h_alert', 'wx_warn_g', 'wx_y', 'wxp29h_title', 'wx_stale', 'wx_err', 'wxp29h_alert', 'wx_p0', 'wxp29h_plong'),
    'weather_27p':    wx('wxp29v', 'wxp29v_neg', 'wxp29v_warn', 'wxp29v_alert', 'wx_warn_g', 'wxp29v_y', 'wxp29v_title', 'wx_stale', 'wx_err', 'wxp29v_alert', 'wxp29v_p0', 'wxp29v_plong'),
    'weather_35':  wx('wx', 'wxneg', 'wx_warn', 'wx_alert', 'wx_warn_g', 'wx_y', 'wx_title', 'wx_stale', 'wx_err', 'wx_alert', 'wx_p0', 'wx_plong'),
    'weather_glance_35':   wx('wx35', 'wx35_neg', 'wx_warn', 'wx35_alert', 'wx_warn_g', 'wx_y', 'wx35_title', 'wx_stale', 'wx_err', 'wx35_alert', 'wx35_p0', 'wx35_plong'),
    'weather_41':   wx('wx42', 'wx42_neg', 'wx42_warn', 'wx42_alert', 'wx42_warn_g', 'wx_y', 'wx42_title', 'wx_stale', 'wx_err', 'wx42_alert', 'wx42_p0', 'wx42_plong'),
    'weather_75':   wx('wx75', 'wx75_negmoon', 'wx75_warn', 'wx75_alert', 'wx75_cond_g', 'wx_y', 'wx75_title', 'wx_stale', 'wx_err', 'wx75_alert', 'wx75_p0', 'wx75_plong'),
    'weather_75p':  wx('wx75p', 'wx75p_negmoon', 'wx75p_warn', 'wx75p_alert', 'wx75p_cond_g', 'wx_y', 'wx75p_title', 'wx_stale', 'wx_err', 'wx75p_alert', 'wx75p_p0', 'wx75p_plong'),
    'weather_calendar_75p':   wx('wxag', 'wxag_widest', 'wxag_warn', 'wxag_widest', 'wxag_g', 'wxag_y', 'wxag_title', 'wxag_stale', 'wxag_err_wx', 'wxag_widest', 'wxag_p0', 'wxag_widest', unav='wxag_unav', empty='wxag_empty'),
    'weather_426':  wx('w426', 'w426_negmoon', 'w426_warn', 'w426_alert', 'w426_warn_g', MONO, 'w426_title', 'w426_stale', 'w426_err', 'w426_alert', 'w426_p0', 'w426_plong', unav='w426_unav'),
    # 'colour' is a panel with a warning colour (BWRY: yellow fills) where the page has a warning level; the scenarios'
    # default panel is BWR. The other pages: n/a where the design system says the state doesn't exist; GAP where no case shows it yet
    'medication_27l':    pg('med29', 'med_widest', 'med_warn', 'med_sev', 'med_warn_g', 'med_sev', 'med29_title', NOSTALE, NOERR, 'med_unav', NOEMPTY),
    'claude_35': pg('claude35', 'claude35_sev', 'claude35_y', 'claude35_sev', 'claude35_sev_g', 'claude35_y', 'claude35_title', 'claude_dead', 'claude_err', 'claude35', NOEMPTY),
    'co2_35':    pg('co2', 'co2_widest', 'co2_warn_y', 'co2_sev', 'co2_warn_y_g', 'co2_warn_y', 'co2_title', 'co2_stale', 'co2_err', 'co2_sev', NOHIST),
    'rain_35':   pg('rain35', 'rain35_widest', 'rain35_warn', 'rain35', 'rain35_g', 'rain35_y', 'rain35_title', 'rain_stale', 'rain_err', 'rain_radar', 'rain_dry'),
    'rain_27l': pg('rain168', 'rain168_widest', 'rain168_warn', 'rain168', 'rain168_g', 'rain168_y', 'rain168_title', 'rain168_stale', 'rain168_err', 'rain168_radar', 'rain168_dry'),
    'sun_moon_35':    pg('sun35', 'sun_widest', NOTHR, NOTHR, NOCHIP, NOCHIP, 'sun35_title', NOSTALE, 'sun_err', 'sun_nomoon', NOEMPTY),
    'entities_35':    pg('entities35', 'ent12', NOTHR, NOTHR, NOCHIP, NOCHIP, 'entities35_title', 'ent_stale', 'ent_err', 'ent_unav', REQ),
    'plants_41': pg('plants42', 'plants20', 'plants42_y', 'plants42', 'plants42_g', 'plants42_y', 'plants42_title', 'plants_stale', 'plants_unav', 'plants42', REQ),
    'doors_windows_14': pg('openings_1', 'openings_3', NOWARN, 'openings_3', 'openings_3_g', 'openings_3', 'openings_1_title', NOSTALE, 'openings_err', 'openings_unav', 'openings_0'),
    # appointment and calendar: no thresholds. An event in progress (NOW) is an ink chip, not a severity (*Severity*, *Now is
    # not a severity*); it is drawn by a35_1now, a41_1now, a426_1now, cal42 and cal426
    # Single value: any sensor; its other configurations (an icon, a second value, a longer reading) are extra cases
    'single_value_14': pg('sv', 'sv_wide4', 'sv_warn', 'sv_sev', 'sv_g', 'sv_y', 'sv_title', 'sv_stale', 'sv_err_long', 'sv_unav', NOEMPTY),
    'single_value_27l': pg('sv', 'sv_widest', 'sv_warn', 'sv_sev', 'sv_g', 'sv_y', 'sv_title', 'sv_stale', NOERRV, 'sv_unav', NOEMPTY),
    'single_value_35': pg('sv', 'sv_widest', 'sv_warn', 'sv_sev', 'sv_g', 'sv_y', 'sv_title', 'sv_stale', NOERRV, 'sv_unav', NOEMPTY),
    # Levels: the first row is required, so the page is never empty
    'levels_27l': pg('lv', 'lv_widest', 'lv_warn', 'lv_sev', 'lv_g', 'lv_y', 'lv_title', 'lv_stale', 'lv_err', 'lv_unav', REQ),
    'levels_35': pg('lv', 'lv_widest', 'lv_warn', 'lv_sev', 'lv_g', 'lv_y', 'lv_title', 'lv_stale', 'lv_err', 'lv_unav', REQ),
    'levels_41': pg('lv', 'lv_widest', 'lv_warn', 'lv_sev', 'lv_g', 'lv_y', 'lv_title', 'lv_stale', 'lv_err', 'lv_unav', REQ),
    # History graph
    'history_27l': pg('hg', 'hg_widest', 'hg_warn', 'hg_sev', 'hg_g', 'hg_y', 'hg_title', 'hg_stale', 'hg_err', 'hg_unav', NOHIST),
    'history_35': pg('hg', 'hg_widest', 'hg_warn', 'hg_sev', 'hg_g', 'hg_y', 'hg_title', 'hg_stale', 'hg_err', 'hg_unav', NOHIST),
    'history_41': pg('hg', 'hg_widest', 'hg_warn', 'hg_sev', 'hg_g', 'hg_y', 'hg_title', 'hg_stale', 'hg_err', 'hg_unav', NOHIST),
    'appointment_35':   pg('appt35', 'a35_1w', NOTHR, NOTHR, NOCHIP, NOCHIP, 'appt35_title', NOSTALE, 'appt35_err', EVENTS, 'appt_none'),
    'appointment_41': pg('a41_6', 'a41_1w', NOTHR, NOTHR, 'a41_6_g', NOCHIP, 'a41_6_title', NOSTALE, 'a41_err', EVENTS, 'a41_0'),
    'appointment_426': pg('a426_9', 'a426_1w', NOTHR, NOTHR, 'a426_9_g', MONO, 'a426_9_title', NOSTALE, 'a426_err', EVENTS, 'a426_0'),
    'calendar_41':    pg('cal42', 'cal_m', NOTHR, NOTHR, NOCHIP, NOCHIP, 'cal42_title', NOSTALE, 'cal42_err', EVENTS, 'cal42_empty'),
    'calendar_426': pg('cal426', 'cal426_m', NOTHR, NOTHR, NOCHIP, MONO, 'cal426_title', NOSTALE, 'cal426_err', EVENTS, 'cal426_empty'),
}


def lint():
    errs, gaps = [], []
    scen = {p.stem for p in (LIB.parent / 'scen').glob('*.py')}
    for key in B:
        cov = COVERAGE.get(key)
        if cov is None:
            errs.append(f'{key}: no coverage entry')
            continue
        need = WX_KINDS if 'alert' in cov else KINDS
        ok = {s for s, b, *_ in CASES if b == key} | (set(WEATHER_EXTRA) if key in EXTRA_KEYS else set())
        for k in need:
            v = cov.get(k)
            if v is None:
                errs.append(f'{key}: kind {k!r} missing')
            elif v == 'GAP':
                gaps.append(f'{key}: {k}')
            elif v.startswith('n/a:'):
                continue
            elif v not in scen:
                errs.append(f'{key}: {k} names {v!r}, which has no scenario file')
            elif v not in ok:
                errs.append(f'{key}: {k} names {v!r}, which is not a check case of this layout')
        if f'pic_{key}' not in ok:
            errs.append(f'{key}: no picture case pic_{key} (its ordinary state in English, for the README: lib/pictures.py)')
        for k in set(cov) - set(need):
            errs.append(f'{key}: unknown kind {k!r}')
    for k in set(COVERAGE) - set(B):
        errs.append(f'{k}: coverage for a layout that does not exist')
    for e in errs:
        print('ERROR ' + e)
    print(f'coverage: {len(B)} layouts, {len(errs)} problems, {len(gaps)} gaps' + (': ' + ', '.join(gaps) if gaps else ''))
    return not errs


if __name__ == '__main__':
    sys.exit(0 if lint() else 1)
