"""Single value: one sensor's number as the hero, its unit beside it (Glance)."""
PAYLOAD_MAIN = r'''
{%- set right = STAMP_AT(ds_last_ts, ds_stale) | float -%}
{%- set v = ds_value -%}
{%- set txt = NUMBER(v.raw) if v.raw else '—' -%}
{%- set second = (NUMBER(v.second) ~ (('¦' ~ v.second_unit) if v.second_unit else '')) if v.second else '' -%}
{#- pattern 'Glance': the hero with its unit; a longer reading than the layout was fitted on steps down the hero ladder -#}
{{- GLANCE(ns, ds_title, right, txt, ds_icon, ds_stale, hlevel=v.level, txt=second, unit=v.unit, step=true) -}}
'''
PAYLOADS = [PAYLOAD_MAIN]
