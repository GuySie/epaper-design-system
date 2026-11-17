PAYLOAD_MAIN = r'''
{%- set W, H, P, TH = EP_TK.width, EP_TK.height, EP_TK.space.pad, EP_TK.space.titleRow -%}
{%- set right = (ds_last_ts | float(0)) if ds_stale else as_timestamp(now()) -%}
{#- pattern 'Key-value list': one column with lines while every row fits, else two columns of equal length; the error state when most values are unavailable -#}
{%- set it = namespace(l=[]) -%}{%- for r in ds_rows -%}{%- set it.l = it.l + [[r.label, r.value, none]] -%}{%- endfor -%}
{{- KVPAGE(ns, header_title_display, right, it.l, ds_stale, ds_rows | rejectattr('ok') | list | length, ds_unavail_msg) -}}
'''

PAYLOAD_ERR = r'''
{%- set W, H, P, TH = EP_TK.width, EP_TK.height, EP_TK.space.pad, EP_TK.space.titleRow -%}
{{- TITLE(ns, header_title_display, as_timestamp(now()), W, P, TH) -}}
{{- ERRBLOCK(ns, language_map[weekday_lang]['no_entities'], W, H, P, TH) -}}
'''
PAYLOADS = [PAYLOAD_MAIN, PAYLOAD_ERR]
