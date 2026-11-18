from _defaults import default
PAYLOAD_MAIN = r'''
{%- set W, H, P, TH = EP_TK.width, EP_TK.height, EP_TK.space.pad, EP_TK.space.titleRow -%}
{%- set right = STAMP_AT(ds_last_ts, ds_stale) | float -%}
{%- set sev = severe_moisture_low | int(''' + str(default('plants', 'severe_moisture_low')) + r''') -%}
{%- set warn = warning_moisture_low | int(''' + str(default('plants', 'warning_moisture_low')) + r''') -%}
{#- the switch (*Thresholds*): off, no plant is flagged -#}
{%- if not (flag_moisture_low | default(true)) -%}{%- set sev, warn = -1, -1 -%}{%- endif -%}
{%- set it = namespace(l=[]) -%}
{%- for p in ds_plants -%}
{%- set val = ((p.pct | string) ~ '%') if p.ok else '—' -%}
{%- set kind = none if not p.ok else ('sev' if p.pct <= sev else ('warn' if p.pct <= warn else none)) -%}
{%- set it.l = it.l + [[p.label, val, kind]] -%}
{%- endfor -%}
{#- the footer's conclusion: how many plants need water, with the right plural (pl/hr have a few/many form) -#}
{%- set cnt = namespace(n=0) -%}{%- for p in ds_plants -%}{%- if p.ok and p.pct <= warn -%}{%- set cnt.n = cnt.n + 1 -%}{%- endif -%}{%- endfor -%}
{%- set wl = language_map[weekday_lang]['needs_water'] -%}
{%- set nn = cnt.n | int -%}
{%- set wi = 0 if nn == 1 else ((1 if (nn % 10 in [2, 3, 4] and nn % 100 not in [12, 13, 14]) else 2) if wl | length == 3 else 1) -%}
{%- set wt = wl[wi] -%}
{%- set foot = (wt | replace('{n}', cnt.n | string) | upper) if cnt.n > 0 else '' -%}
{%- set unav = language_map[weekday_lang]['most_unavailable'] -%}
{#- pattern 'Key-value list', dense rows; the error state when most values are unavailable -#}
{{- KVPAGE(ns, header_title_display, right, it.l, ds_stale, ds_plants | rejectattr('ok') | list | length, unav, true, foot) -}}
'''

PAYLOAD_ERR = r'''
{{- ERRPAGE(ns, header_title_display, language_map[weekday_lang]['no_plants']) -}}
'''
PAYLOADS = [PAYLOAD_MAIN, PAYLOAD_ERR]
