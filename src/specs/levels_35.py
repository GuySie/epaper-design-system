"""Levels: up to four (on the 4.1" six) sensors as rows with their value and a bar (Meters)."""
PAYLOAD_MAIN = r'''
{%- set right = STAMP_AT(ds_last_ts, ds_stale) | float -%}
{#- the number as it is read: no decimals from 100 up or when it has none, else one -#}
{%- macro NUM(raw) -%}{%- set n = raw | float(none) -%}{{ raw if n is none else DECIMAL(((n | round(0) | int) if (n | abs >= 100 or n == (n | round(0))) else (n | round(1))) | string) }}{%- endmacro -%}
{%- set rows = ds_levels -%}
{%- set n = rows | length -%}
{%- set bad = rows | rejectattr('ok') | list | length -%}
{%- if n >= 2 and bad * 2 > n -%}
{#- mostly unavailable (*States*): the error state -#}
{{- ERRPAGE(ns, header_title_display, language_map[weekday_lang]['most_unavailable']) -}}
{%- else -%}
{%- set bl = namespace(l=[]) -%}
{%- for r in rows -%}
{%- set txt = (NUM(r.raw) ~ (('¦' ~ r.unit) if r.unit else '')) if r.ok else '--' -%}
{%- set bl.l = bl.l + [{'label': r.label, 'percent': r.pct, 'percent_text': txt, 'marker_pct': none, 'is_severe': r.level == 'sev', 'is_warning': r.level == 'warn', 'rcap': ''}] -%}
{%- endfor -%}
{#- pattern 'Meters', without a footer -#}
{{- METERS(ns, header_title_display, right, bl.l, ds_stale) -}}
{%- endif -%}
'''
PAYLOADS = [PAYLOAD_MAIN]
