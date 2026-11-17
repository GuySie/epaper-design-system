PAYLOAD_MAIN = r'''
{%- set W, H, P, TH = EP_TK.width, EP_TK.height, EP_TK.space.pad, EP_TK.space.titleRow -%}
{%- set north = hemisphere == 'northern' -%}
{%- set moon = {'az': states(moon_azimuth_sensor), 'alt': states(moon_altitude_sensor), 'icon': 'mdi:' ~ (moon_icon | trim if moon_phase_available else 'moon-waxing-crescent')} if moon_position_available else none -%}
{%- set times = namespace(l=[]) -%}
{%- for k in ['next_dawn', 'next_rising', 'next_noon', 'next_setting', 'next_dusk'] -%}
{#- 12-hour: am/pm set as a unit (*Sun & moon*, times follow time_format) -#}
{%- set ts = as_timestamp(state_attr('sun.sun', k)) -%}
{%- set times.l = times.l + [[ds_txt['t'][loop.index0] | upper, (ts | timestamp_custom('%H:%M')) if time_format == '24h' else (ts | timestamp_custom('%-I:%M')) ~ '¦' ~ (ts | timestamp_custom('%p') | lower)]] -%}
{%- endfor -%}
{#- footer: day length (the moon phase is on the timeline) -#}
{%- set r = as_timestamp(state_attr('sun.sun', 'next_rising')) -%}
{%- set s = as_timestamp(state_attr('sun.sun', 'next_setting')) -%}
{%- set dl = (s - r) if s > r else (s - (r - 86400)) -%}
{%- set dls = (dl // 3600) | int ~ '¦h¦' ~ ('%02d' | format(((dl % 3600) // 60) | int)) ~ '¦min' -%}
{#- pattern 'Timeline': sun and moon on the compass axis, the five times of the day, the day length in the footer -#}
{{- TIMELINE(ns, header_title_display, as_timestamp(now()), state_attr('zone.home', 'latitude') | float(52), north, state_attr('sun.sun', 'azimuth') | float(0), state_attr('sun.sun', 'elevation') | float(0), moon,
     [ds_txt['c'][0], ds_txt['c'][1], ds_txt['c'][2]] if north else [ds_txt['c'][0], ds_txt['c'][3], ds_txt['c'][2]], times.l, (ds_txt['dl'] | upper) ~ ' ' ~ dls) -}}
'''

PAYLOAD_ERR = r'''
{{- ERRPAGE(ns, header_title_display, language_map[weekday_lang]['no_sun']) -}}
'''
PAYLOADS = [PAYLOAD_MAIN, PAYLOAD_ERR]
