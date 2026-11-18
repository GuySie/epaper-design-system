"""Value with details: one sensor's value large, other values beside it, its last hours as a line under it (Hero dashboard
with a chart or list). The drawing every screen shares."""
WIDEST = '-12.5'      # the widest number the hero and the chart's labels can have: four characters with a decimal and a sign
LABEL = 'Temperature'  # the widest label a detail row is drawn for (11 characters); a longer one is cut
PAYLOAD_MAIN = r"""
{%- set W, H, P, TH = EP_TK.width, EP_TK.height, EP_TK.space.pad, EP_TK.space.titleRow -%}
{%- set right = STAMP_AT(ds_last_ts, ds_stale) | float -%}
{%- set h12 = time_format != '24h' -%}
{%- set v = ds_value -%}
{%- set rows = namespace(l=[]) -%}
{%- for d in ds_details -%}{%- set rows.l = rows.l + [[d.label, (READING(d.raw, d.unit) if d.ok else '—'), '']] -%}{%- endfor -%}
{%- set h = {'text': (NUMBER(v.raw) if v.raw else '—'), 'level': v.level, 'icon': ds_icon | default(''), 'bare': not v.raw, 'moon': false, 'widest': DECIMAL(""" + repr(WIDEST) + r"""), 'unit': v.unit} -%}
{#- an unavailable sensor is a dash on its own: no unit, and its icon is not drawn (bare) though it keeps its room in the height -#}
{%- set pts = ds_pts -%}
{#- pattern 'Hero dashboard' with a chart: the detail column is as wide as the widest label and the widest value a row is drawn for -#}
{%- call(top, bottom) HERODASH(ns, ds_title, right, ds_stale, h, rows.l, none, [], [""" + repr(LABEL) + r"""], [DECIMAL(""" + repr(WIDEST) + r""") ~ '°C', '1240¦ppm']) -%}
{%- if pts | length >= 2 -%}
{%- set mm = namespace(lo=pts[0].mn, hi=pts[0].mx) -%}
{%- for p in pts -%}{%- set mm.lo, mm.hi = [mm.lo, p.mn] | min, [mm.hi, p.mx] | max -%}{%- endfor -%}
{#- one decimal while the values stay under 100, none from there; the automatic scale takes in every value and every threshold line that is shown -#}
{%- set dec = 1 if ([mm.lo | abs, mm.hi | abs] | max) < 100 else 0 -%}
{%- set fh, fl = flag_high | default(false), flag_low | default(false) -%}
{%- set wh, sh, wl, sl = warning_high | float(0), severe_high | float(0), warning_low | float(0), severe_low | float(0) -%}
{%- set inl = [mm.lo, mm.hi] + ([wh, sh] if fh else []) + ([wl, sl] if fl else []) -%}
{%- set sc = CHART_SCALE(inl | min, inl | max, dec).split(',') | map('float') | list -%}
{{- CHART_LINE(ns, P, W - P - 1, top, bottom - 1, pts, ds_t0 | float, ds_t1 | float, sc[0], sc[1], wh, sh, 900 * (ds_bucket | int(1)), h12, fh,
               {'ends': true, 'dec': dec, 'low': ([wl, sl] if fl else none), 'widest': DECIMAL(""" + repr(WIDEST) + r""")}) -}}
{%- else -%}
{#- no history: the error block in the chart's half; the number and its details keep drawing -#}
{{- ERRBLOCK(ns, language_map[weekday_lang]['no_data'], W, H, P, TH, top, bottom) -}}
{%- endif -%}
{%- endcall -%}
"""
PAYLOADS = [PAYLOAD_MAIN]
