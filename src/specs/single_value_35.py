"""Single value: one sensor's number as the hero, its unit beside it (Glance)."""
PAYLOAD_MAIN = r'''
{%- set right = STAMP_AT(ds_last_ts, ds_stale) | float -%}
{%- set v = ds_value -%}
{%- set txt = NUMBER(v.raw) if v.raw else '—' -%}
{%- set second = (NUMBER(v.second) ~ (('¦' ~ v.second_unit) if v.second_unit else '')) if v.second else '' -%}
{%- set W, P = EP_TK.width, EP_TK.space.pad -%}
{%- if v.raw and (HERO_INK_W(txt, HUP.keys() | list | sort | first) | int) + (HERO_UNIT_W(v.unit) | int) > W - 2 * P -%}
{#- a reading too wide for the smallest rung is never cut: it is the error state (*Single value*, Widest reading) -#}
{{- ERRPAGE(ns, ds_title, language_map[weekday_lang]['too_long']) -}}
{%- else -%}
{#- pattern 'Glance': the hero with its unit; a longer reading than the layout was fitted on steps down the hero ladder -#}
{{- GLANCE(ns, ds_title, right, txt, ds_icon, ds_stale, hlevel=v.level, txt=second, unit=v.unit, step=true) -}}
{%- endif -%}
'''
PAYLOADS = [PAYLOAD_MAIN]
