"""Single value on the 1.4": the number as the hero at one size, its unit as the Glance secondary (the screen is too
narrow for a unit beside a four-digit number); no second value. A reading too wide for the screen is the error view."""
PAYLOAD_MAIN = r'''
{#- follows *Single value*, *The 1.4" has one size* -#}
{%- set W, P = EP_TK.width, EP_TK.space.pad -%}
{%- set right = STAMP_AT(ds_last_ts, ds_stale) | float -%}
{%- set v = ds_value -%}
{%- set txt = NUMBER(v.raw) if v.raw else '—' -%}
{%- if v.raw and (HERO_INK_W(txt, EP_TK.type.heroAlone) | int) > W - 2 * P -%}
{#- the hero has one size here, fitted on four digits: a longer reading doesn't step down, it says so -#}
{{- ERRPAGE(ns, ds_title, language_map[weekday_lang]['too_long']) -}}
{%- else -%}
{#- pattern 'Glance': the unit is the Glance secondary -#}
{{- GLANCE(ns, ds_title, right, txt, ds_icon, ds_stale, hlevel=v.level, txt=v.unit) -}}
{%- endif -%}
'''
PAYLOADS = [PAYLOAD_MAIN]
