"""History graph: one sensor's last hours as a line on the automatic scale (Line chart). The drawing every screen shares."""
WIDEST = '-12.5'      # the widest value label the page can have: four characters with a decimal and a sign
PAYLOAD_MAIN = r'''
{%- set right = STAMP_AT(ds_last_ts, ds_stale) | float -%}
{%- set h12 = time_format != '24h' -%}
{%- set pts = ds_pts -%}
{%- set mm = namespace(lo=pts[0].mn, hi=pts[0].mx) -%}
{%- for p in pts -%}{%- set mm.lo, mm.hi = [mm.lo, p.mn] | min, [mm.hi, p.mx] | max -%}{%- endfor -%}
{#- one decimal while the values stay under 100, none from there -#}
{%- set dec = 1 if ([mm.lo | abs, mm.hi | abs] | max) < 100 else 0 -%}
{%- macro NUM(v) -%}{{ DECIMAL(((v | round(dec)) | string).replace('.0', '')) if dec else (v | round | int) }}{%- endmacro -%}
{#- the automatic scale takes in every value and every threshold line that is shown -#}
{%- set fh, fl = flag_high | default(false), flag_low | default(false) -%}
{%- set wh, sh, wl, sl = warning_high | float(0), severe_high | float(0), warning_low | float(0), severe_low | float(0) -%}
{%- set inl = [mm.lo, mm.hi] + ([wh, sh] if fh else []) + ([wl, sl] if fl else []) -%}
{%- set sc = CHART_SCALE(inl | min, inl | max, dec).split(',') | map('float') | list -%}
{%- set last = pts[-1] -%}
{%- set lt = language_map[weekday_lang] -%}
{%- set u = ('¦' ~ ds_unit) if ds_unit else '' -%}
{%- set left = lt['now'] ~ ' ' ~ NUM(last.v) ~ u -%}
{%- set rt = lt['low'] ~ ' ' ~ NUM(mm.lo) ~ ' · ' ~ lt['high'] ~ ' ' ~ NUM(mm.hi) ~ u -%}
{%- set kind = 'sev' if ((fh and mm.hi >= sh) or (fl and mm.lo <= sl)) else ('warn' if ((fh and mm.hi >= wh) or (fl and mm.lo <= wl)) else none) -%}
{#- pattern 'Line chart': the last hours, the current value as a square at the end -#}
{{- LINECHART(ns, ds_title, right, pts, ds_t0 | float, ds_t1 | float, sc[0], sc[1], wh, sh, 900 * (ds_bucket | int(1)), [left, rt, kind], h12, ds_stale, fh,
              {'ends': true, 'dec': dec, 'low': ([wl, sl] if fl else none), 'widest': DECIMAL(''' + repr(WIDEST) + r''')}) -}}
'''
PAYLOAD_ERR = r'''
{{- ERRPAGE(ns, ds_title, language_map[weekday_lang]['no_data']) -}}
'''
PAYLOADS = [PAYLOAD_MAIN, PAYLOAD_ERR]
