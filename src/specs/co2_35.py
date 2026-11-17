from _defaults import default
SCALE_FROM = 400        # ppm: outdoor air, which indoor air rarely goes below (*Chart frame (all charts)*, *Fixed y-scale*)
PAYLOAD_MAIN = r'''
{%- set W, H, P, TH = EP_TK.width, EP_TK.height, EP_TK.space.pad, EP_TK.space.titleRow -%}
{%- set h12 = time_format != '24h' -%}
{%- set right = STAMP_AT(ds_last_ts, ds_stale) | float -%}
{%- set warn, sev = warning_co2 | float(''' + str(default('co2', 'warning_co2')) + r'''), severe_co2 | float(''' + str(default('co2', 'severe_co2')) + r''') -%}
{#- scale, set by the CO2 page: from outdoor air (SCALE_FROM) up to EP_CHART.top x the severe value -#}
{%- set lo = ''' + str(SCALE_FROM) + r''' -%}
{%- set hi = [sev * EP_CHART.top, lo + 100] | max -%}
{%- set last = ds_pts[-1] -%}
{#- summary: current value and the peak with its clock time; a chip when the peak crossed a threshold -#}
{%- set pk = namespace(v=0, ts=0) -%}
{%- for p in ds_pts -%}{%- if p.mx > pk.v -%}{%- set pk.v, pk.ts = p.mx, p.ts -%}{%- endif -%}{%- endfor -%}
{%- set lt = language_map[weekday_lang] -%}
{%- set left = lt['now'] ~ ' ' ~ (last.v | round | int) ~ '¦ppm' -%}
{%- set rt = lt['peak'] ~ ' ' ~ (pk.v | round | int) ~ '¦ppm¦ · ' ~ CLOCK(pk.ts, h12) -%}
{%- set flag = flag_co2 | default(true) -%}
{%- set kind = ('sev' if pk.v >= sev else ('warn' if pk.v >= warn else none)) if flag else none -%}
{#- pattern 'Line chart' with thresholds: the last hours of CO2, the current value as a square at the end -#}
{{- LINECHART(ns, ds_title, right, ds_pts, ds_t0 | float, ds_t1 | float, lo, hi, warn, sev, 900 * (ds_bucket | int(1)), [left, rt, kind], h12, ds_stale, flag) -}}
'''

PAYLOAD_ERR = r'''
{{- ERRPAGE(ns, ds_title, language_map[weekday_lang]['no_data']) -}}
'''
PAYLOADS = [PAYLOAD_MAIN, PAYLOAD_ERR]
