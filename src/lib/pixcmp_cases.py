"""The one list of check cases: the blueprint map, the cases (scenario, blueprint, gap rule, bottom rule), the canvas sizes and
the weather extras. check.py, baseline.py, layout_fit.py, coverage.py, registry.py and shared.py all read it; a new case goes
here only, and its kind of state into coverage.py."""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from layouts import layouts            # noqa: E402  the one list of layouts (pages/*.yaml)
B = {l['key']: l['blueprint'] for l in layouts()}       # layout key -> blueprint file
CASES = [
    ('wxp16', 'weather_glance_14', 'skip', 'free'), ('wxp16_alert', 'weather_glance_14', 'skip', 'free'), ('wxp16_pol', 'weather_glance_14', 'skip', 'free'), ('wxp29v_fog', 'weather_27p', 'C', 'fill'), ('wxp29v_cond', 'weather_27p', 'C', 'fill'), ('wxp16_alert_y', 'weather_glance_14', 'skip', 'free'), ('wxp16_y', 'weather_glance_14', 'skip', 'free'), ('wxp16b', 'weather_glance_14', 'skip', 'free'), ('wxneg16', 'weather_glance_14', 'skip', 'free'),
    ('med29', 'medication_27l', 'skip', 'free'), ('med_warn', 'medication_27l', 'skip', 'free'), ('med_sev', 'medication_27l', 'skip', 'free'), ('wxp16_warn', 'weather_glance_14', 'skip', 'free'),
    ('wxp29h', 'weather_27l', 'C', 'fill'), ('wxp29h_alert', 'weather_27l', 'C', 'fill'), ('wxp29h_neg', 'weather_27l', 'C', 'fill'),
    ('wxp29v', 'weather_27p', 'C', 'fill'), ('wxp29v_alert', 'weather_27p', 'C', 'fill'), ('wxp29v_warn', 'weather_27p', 'C', 'fill'), ('wxp29v_np', 'weather_27p', 'C', 'fill'), ('wxp29v_y', 'weather_27p', 'C', 'fill'),
    ('appt35', 'appointment_35', 'skip', 'free'), ('a35_1now', 'appointment_35', 'M', 'fill'),
    ('claude35', 'claude_35', 'M', 'free'), ('claude35_y', 'claude_35', 'M', 'free'), ('claude35_sev', 'claude_35', 'M', 'free'),
    ('claude_dead', 'claude_35', 'M', 'free'),
    ('co2', 'co2_35', 'M', 'fill'), ('co2_sev', 'co2_35', 'M', 'fill'), ('co2_warn_y', 'co2_35', 'M', 'fill'), ('co2_err', 'co2_35', 'skip', 'free'),
    ('entities35', 'entities_35', 'M', 'free'), ('ent12', 'entities_35', 'M', 'free'), ('ent_unav', 'entities_35', 'skip', 'free'), ('ent_err', 'entities_35', 'skip', 'free'), ('ent_stale', 'entities_35', 'M', 'free'),
    ('rain35', 'rain_35', 'skip', 'fill'), ('rain35_y', 'rain_35', 'skip', 'fill'), ('rain_stale', 'rain_35', 'skip', 'fill'),
    ('rain168', 'rain_27l', 'skip', 'fill'), ('rain_radar', 'rain_35', 'skip', 'fill'), ('claude_reset', 'claude_35', 'M', 'free'), ('co2_stale', 'co2_35', 'M', 'fill'), ('plants_stale', 'plants_41', 'M', 'free'), ('rain_err', 'rain_35', 'skip', 'free'),
    ('sun35', 'sun_moon_35', 'skip', 'fill'), ('sun_night', 'sun_moon_35', 'skip', 'fill'), ('sun_noon', 'sun_moon_35', 'skip', 'fill'), ('sun_letter', 'sun_moon_35', 'skip', 'fill'), ('sun_south', 'sun_moon_35', 'skip', 'fill'), ('sun_summer', 'sun_moon_35', 'skip', 'fill'), ('sun_newmoon', 'sun_moon_35', 'skip', 'fill'),
    ('wx35', 'weather_glance_35', 'skip', 'free'), ('wx35_alert', 'weather_glance_35', 'skip', 'free'),
    ('wx_cond', 'weather_35', 'C', 'fill'), ('wx42_cond', 'weather_41', 'C', 'fill'),('wxp16_cond', 'weather_glance_14', 'skip', 'free'), ('wx75_cond', 'weather_75', 'C', 'free'), ('wx', 'weather_35', 'C', 'fill'), ('wx_alert', 'weather_35', 'C', 'fill'), ('wx_warn', 'weather_35', 'C', 'fill'), ('wx_y', 'weather_35', 'C', 'fill'), ('wxneg', 'weather_35', 'C', 'fill'),
    ('cal42', 'calendar_41', 'skip', 'free'), ('cal_m', 'calendar_41', 'skip', 'free'),
    ('a426_9', 'appointment_426', 'M', 'free'), ('a426_6', 'appointment_426', 'M', 'fill'), ('a426_3', 'appointment_426', 'M', 'fill'), ('a426_1', 'appointment_426', 'M', 'fill'), ('a426_1now', 'appointment_426', 'M', 'fill'), ('a426_0', 'appointment_426', 'skip', 'free'),
    ('cal426', 'calendar_426', 'skip', 'free'), ('cal426_m', 'calendar_426', 'skip', 'free'), ('appt_m', 'appointment_35', 'M', 'free'),
    ('wx_p0', 'weather_35', 'C', 'fill'), ('wx42_p0', 'weather_41', 'C', 'fill'), ('wxp29v_p0', 'weather_27p', 'C', 'fill'), ('rain_dry', 'rain_35', 'skip', 'free'), ('claude_m', 'claude_35', 'M', 'fill'),
    ('plants20', 'plants_41', 'M', 'fill'), ('appt_3', 'appointment_35', 'M', 'fill'), ('a41_6', 'appointment_41', 'M', 'fill'), ('a41_3', 'appointment_41', 'M', 'fill'), ('a41_1', 'appointment_41', 'M', 'fill'), ('a41_1now', 'appointment_41', 'M', 'fill'), ('a41_0', 'appointment_41', 'skip', 'free'), ('co2_warn_y_g', 'co2_35', 'M', 'fill'), ('claude35_sev_g', 'claude_35', 'M', 'free'), ('rain35_g', 'rain_35', 'skip', 'fill'), ('plants42_g', 'plants_41', 'M', 'free'), ('wx75_cond_g', 'weather_75', 'C', 'free'), ('wx_warn_g', 'weather_35', 'C', 'fill'), ('a41_6_g', 'appointment_41', 'M', 'fill'), ('wxp16_warn_g', 'weather_glance_14', 'skip', 'free'), ('wx42_warn_g', 'weather_41', 'C', 'fill'),
    ('plants42', 'plants_41', 'M', 'free'), ('plants42_y', 'plants_41', 'M', 'free'),
    ('wx42', 'weather_41', 'C', 'fill'), ('wx42_alert', 'weather_41', 'C', 'fill'), ('wx42_warn', 'weather_41', 'C', 'fill'),
    ('wx_moon', 'weather_35', 'C', 'fill'), ('wx35_moon', 'weather_glance_35', 'skip', 'free'), ('wxp16_moon', 'weather_glance_14', 'skip', 'free'), ('wxp16_10', 'weather_glance_14', 'skip', 'free'), ('wx75_moon', 'weather_75', 'C', 'free'), ('wxp29v_moon', 'weather_27p', 'C', 'fill'),
    ('openings_0', 'doors_windows_14', 'skip', 'free'), ('openings_1', 'doors_windows_14', 'skip', 'free'), ('openings_3', 'doors_windows_14', 'skip', 'free'), ('openings_2en', 'doors_windows_14', 'skip', 'free'),
    ('w426', 'weather_426', 'C', 'free'), ('w426_alert', 'weather_426', 'C', 'free'), ('w426_cond', 'weather_426', 'C', 'free'), ('w426_moon', 'weather_426', 'C', 'free'), ('w426neg', 'weather_426', 'C', 'free'), ('w426_title', 'weather_426', 'C', 'free'),
    ('wx75', 'weather_75', 'C', 'free'), ('wx75_alert', 'weather_75', 'C', 'free'), ('wx75neg', 'weather_75', 'C', 'free'), ('wx75_title', 'weather_75', 'C', 'free'),
    ('wx75p', 'weather_75p', 'C', 'fill'), ('wx75p_alert', 'weather_75p', 'C', 'fill'), ('wx75p_cond', 'weather_75p', 'C', 'fill'), ('wx75p_cond_g', 'weather_75p', 'C', 'fill'),
    ('wx75p_moon', 'weather_75p', 'C', 'fill'), ('wx75p_neg', 'weather_75p', 'C', 'fill'), ('wx75p_negmoon', 'weather_75p', 'C', 'fill'), ('wx75p_title', 'weather_75p', 'C', 'fill'),
    # the widest pollen row with an alert row: both take a detail row's place
    ('wxp16_plong', 'weather_glance_14', 'skip', 'free'), ('wx35_plong', 'weather_glance_35', 'skip', 'free'), ('wxp29v_plong', 'weather_27p', 'C', 'fill'), ('med_widest', 'medication_27l', 'skip', 'free'), ('med_12h_widest', 'medication_27l', 'skip', 'free'), ('co2_widest', 'co2_35', 'M', 'fill'), ('rain35_warn', 'rain_35', 'skip', 'fill'), ('rain168_warn', 'rain_27l', 'skip', 'fill'), ('rain35_widest', 'rain_35', 'skip', 'fill'), ('rain168_widest', 'rain_27l', 'skip', 'fill'), ('sun_widest', 'sun_moon_35', 'skip', 'fill'), ('cal42_sv', 'calendar_41', 'skip', 'free'), ('cal426_pl', 'calendar_426', 'skip', 'free'), ('appt35_hr', 'appointment_35', 'skip', 'free'), ('a41_6_fr', 'appointment_41', 'M', 'fill'), ('a426_9_es', 'appointment_426', 'M', 'free'), ('wx_plong', 'weather_35', 'C', 'fill'), ('wx42_plong', 'weather_41', 'C', 'fill'), ('wxp29h_plong', 'weather_27l', 'C', 'fill'), ('wx75_plong', 'weather_75', 'C', 'free'), ('wx75p_plong', 'weather_75p', 'C', 'fill'), ('w426_plong', 'weather_426', 'C', 'free'),
    # a typed title longer than the title room, on every layout (cut before the stamp)
    ('wxp16_title', 'weather_glance_14', 'skip', 'free'), ('wxp29h_title', 'weather_27l', 'C', 'fill'), ('wxp29v_title', 'weather_27p', 'C', 'fill'), ('wx_title', 'weather_35', 'C', 'fill'), ('wx35_title', 'weather_glance_35', 'skip', 'free'), ('wx42_title', 'weather_41', 'C', 'fill'), ('med29_title', 'medication_27l', 'skip', 'free'), ('claude35_title', 'claude_35', 'M', 'free'), ('co2_title', 'co2_35', 'M', 'fill'), ('rain35_title', 'rain_35', 'skip', 'fill'), ('rain168_title', 'rain_27l', 'skip', 'fill'), ('sun35_title', 'sun_moon_35', 'skip', 'fill'), ('entities35_title', 'entities_35', 'M', 'free'), ('plants42_title', 'plants_41', 'M', 'free'), ('openings_1_title', 'doors_windows_14', 'skip', 'free'), ('appt35_title', 'appointment_35', 'skip', 'free'), ('a41_6_title', 'appointment_41', 'M', 'fill'), ('a426_9_title', 'appointment_426', 'M', 'free'), ('cal42_title', 'calendar_41', 'skip', 'free'), ('cal426_title', 'calendar_426', 'skip', 'free'),
    # error views, stale and a yellow panel where a layout had none
    ('appt35_err', 'appointment_35', 'skip', 'free'), ('a41_err', 'appointment_41', 'skip', 'free'), ('a426_err', 'appointment_426', 'skip', 'free'), ('cal42_err', 'calendar_41', 'skip', 'free'), ('cal426_err', 'calendar_426', 'skip', 'free'), ('claude_err', 'claude_35', 'skip', 'free'), ('openings_err', 'doors_windows_14', 'skip', 'free'), ('sun_err', 'sun_moon_35', 'skip', 'free'), ('rain168_err', 'rain_27l', 'skip', 'free'), ('w426_err', 'weather_426', 'skip', 'free'), ('rain168_stale', 'rain_27l', 'skip', 'fill'), ('w426_stale', 'weather_426', 'C', 'free'), ('rain168_y', 'rain_27l', 'skip', 'fill'),
    # Weather and calendar (7.5" portrait): the hero band over the date-grouped list
    ('wxag', 'weather_calendar_75p', 'C', 'free'), ('wxag_widest', 'weather_calendar_75p', 'C', 'free'), ('wxag_now', 'weather_calendar_75p', 'C', 'free'), ('wxag_warn', 'weather_calendar_75p', 'C', 'free'), ('wxag_g', 'weather_calendar_75p', 'C', 'free'), ('wxag_y', 'weather_calendar_75p', 'C', 'free'), ('wxag_title', 'weather_calendar_75p', 'C', 'free'), ('wxag_stale', 'weather_calendar_75p', 'C', 'free'), ('wxag_p0', 'weather_calendar_75p', 'C', 'free'), ('wxag_err_wx', 'weather_calendar_75p', 'skip', 'free'), ('wxag_err_cal', 'weather_calendar_75p', 'C', 'free'), ('wxag_over', 'weather_calendar_75p', 'C', 'free'), ('wxag_empty', 'weather_calendar_75p', 'C', 'free'),
    # pollen on every weather layout: at 0 (no pollen row) and at warning level
    ('wx75_p0', 'weather_75', 'C', 'free'), ('wx75_warn', 'weather_75', 'C', 'free'), ('wx75p_p0', 'weather_75p', 'C', 'fill'), ('wx75p_warn', 'weather_75p', 'C', 'fill'),
    ('w426_p0', 'weather_426', 'C', 'free'), ('w426_warn', 'weather_426', 'C', 'free'), ('wx35_p0', 'weather_glance_35', 'skip', 'free'),
    # the widest reading (-12°) and the moon badge on every weather layout (hero group)
    ('wxp29v_neg', 'weather_27p', 'C', 'fill'), ('wx35_neg', 'weather_glance_35', 'skip', 'free'), ('wx42_neg', 'weather_41', 'C', 'fill'),
    ('wxp29h_moon', 'weather_27l', 'C', 'fill'), ('wxp29h_negmoon', 'weather_27l', 'C', 'fill'), ('wx75_negmoon', 'weather_75', 'C', 'free'),
    ('w426_negmoon', 'weather_426', 'C', 'free'), ('wxp16_negmoon', 'weather_glance_14', 'skip', 'free'),
    ('ent_units', 'entities_35', 'M', 'free'),   # units as Home Assistant writes them: every glyph must exist in TRMNL
    ('plants_unav', 'plants_41', 'skip', 'free'),   # plants' error state when most values are unavailable
    # unavailable values and empty states where a layout had no case (coverage kinds 'unavailable', 'empty')
    ('w426_unav', 'weather_426', 'C', 'free'), ('wxag_unav', 'weather_calendar_75p', 'C', 'free'), ('med_unav', 'medication_27l', 'skip', 'free'), ('sun_nomoon', 'sun_moon_35', 'skip', 'fill'),
    ('openings_unav', 'doors_windows_14', 'skip', 'free'), ('rain168_radar', 'rain_27l', 'skip', 'fill'), ('rain168_dry', 'rain_27l', 'skip', 'free'),
    # a blueprint and templates from different releases (Blueprint mechanics, One set), on the tightest, a medium and a large screen
    ('set_err_14', 'weather_glance_14', 'skip', 'free'), ('set_err_35', 'co2_35', 'skip', 'free'), ('set_err_75', 'weather_75', 'skip', 'free'),
    # the event hero's widest reading (20:00) on each screen, and the 3.5" event hero before it starts
    ('a35_1w', 'appointment_35', 'M', 'fill'), ('a41_1w', 'appointment_41', 'M', 'fill'), ('a426_1w', 'appointment_426', 'M', 'fill'), ('a35_1', 'appointment_35', 'M', 'fill'),
    # a reading's switch off (*Thresholds*): nothing is flagged
    ('claude35_flagoff', 'claude_35', 'M', 'free'), ('plants42_flagoff', 'plants_41', 'M', 'free'), ('med_flagoff', 'medication_27l', 'skip', 'free'),
    ('rain35_flagoff', 'rain_35', 'skip', 'fill'), ('rain168_flagoff', 'rain_27l', 'skip', 'fill'), ('co2_flagoff', 'co2_35', 'M', 'fill'),
    # 12-hour time on a chart (*Chart frame (all charts)*, Clock-time axis): am/pm on every axis label and in the footer
    ('rain35_12h', 'rain_35', 'skip', 'fill'), ('rain35_12h_noon', 'rain_35', 'skip', 'fill'), ('rain35_12h_dry', 'rain_35', 'skip', 'free'),
    ('rain168_12h', 'rain_27l', 'skip', 'fill'), ('rain168_12h_noon', 'rain_27l', 'skip', 'fill'), ('co2_12h_widest', 'co2_35', 'M', 'fill'),
    # a grayscale panel on the screens that had no such case (every screen has one: lib/coverage.py)
    ('med_warn_g', 'medication_27l', 'skip', 'free'), ('rain168_g', 'rain_27l', 'skip', 'fill'), ('openings_3_g', 'doors_windows_14', 'skip', 'free'),
    ('w426_warn_g', 'weather_426', 'C', 'free'), ('a426_9_g', 'appointment_426', 'M', 'free'),
    ('cal42_empty', 'calendar_41', 'skip', 'free'), ('cal426_empty', 'calendar_426', 'skip', 'free'), ('appt_none', 'appointment_35', 'skip', 'free'),
    # the reference pictures (lib/pictures.py): each layout's ordinary state in English, `pic_<layout>`
    ('pic_appointment_35', 'appointment_35', 'skip', 'free'), ('pic_appointment_41', 'appointment_41', 'M', 'fill'), ('pic_appointment_426', 'appointment_426', 'M', 'free'),
    ('pic_calendar_41', 'calendar_41', 'skip', 'free'), ('pic_calendar_426', 'calendar_426', 'skip', 'free'), ('pic_claude_35', 'claude_35', 'M', 'free'),
    ('pic_co2_35', 'co2_35', 'M', 'fill'), ('pic_doors_windows_14', 'doors_windows_14', 'skip', 'free'), ('pic_entities_35', 'entities_35', 'M', 'free'),
    ('pic_medication_27l', 'medication_27l', 'skip', 'free'), ('pic_plants_41', 'plants_41', 'M', 'free'), ('pic_rain_35', 'rain_35', 'skip', 'fill'),
    ('pic_rain_27l', 'rain_27l', 'skip', 'fill'), ('pic_sun_moon_35', 'sun_moon_35', 'skip', 'fill'), ('pic_weather_calendar_75p', 'weather_calendar_75p', 'C', 'free'),
    ('pic_weather_glance_14', 'weather_glance_14', 'skip', 'free'), ('pic_weather_glance_35', 'weather_glance_35', 'skip', 'free'), ('pic_weather_27l', 'weather_27l', 'C', 'fill'),
    ('pic_weather_27p', 'weather_27p', 'C', 'fill'), ('pic_weather_35', 'weather_35', 'C', 'fill'), ('pic_weather_41', 'weather_41', 'C', 'fill'),
    ('pic_weather_426', 'weather_426', 'C', 'free'), ('pic_weather_75', 'weather_75', 'C', 'free'), ('pic_weather_75p', 'weather_75p', 'C', 'fill'),
]

SIZES = {l['key']: l['canvas'] for l in layouts()}      # layout key -> canvas (its screen's tier)
WEATHER_EXTRA = ['wx', 'wx_cond', 'wx_alert', 'wx_warn', 'wx_y', 'wxneg', 'wx_p0', 'wx_warn_g', 'wx_moon', 'tonight', 'tonight_knmi', 'tonight_knmi2',
                 'tonight_knmi3', 'tonight_storm', 'wx_bw', 'wx_12h_en', 'wx_stale', 'wx_err', 'wx_unav', 'wx_flagoff']

# the weather extras run on every weather layout below, at the layout's canvas size (check.py and baseline.py inject it),
# with the layout's own gap and bottom rules; the error view is a centred block (no gap or bottom rule)
EXTRA_KEYS = ('weather_glance_14', 'weather_27l', 'weather_27p', 'weather_35', 'weather_glance_35', 'weather_41', 'weather_75', 'weather_75p')
_RULES = {'weather_glance_14': ('skip', 'free'), 'weather_27l': ('C', 'fill'), 'weather_27p': ('C', 'fill'), 'weather_35': ('C', 'fill'), 'weather_glance_35': ('skip', 'free'),
          'weather_41': ('C', 'fill'), 'weather_75': ('C', 'free'), 'weather_75p': ('C', 'fill')}
EXTRA_CASES = [(s, key) + (('skip', 'free') if s == 'wx_err' else _RULES[key])
               for key in EXTRA_KEYS for s in WEATHER_EXTRA if s not in {c[0] for c in CASES if c[1] == key}]
