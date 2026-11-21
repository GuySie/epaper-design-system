"""Room sign: one entity's state as a word, an optional second entity under it (Glance with a word). The drawing every screen shares."""
PAYLOAD_MAIN = r"""
{%- set v = ds_room -%}
{%- set second = ((NUMBER(v.second) ~ (('¦' ~ v.second_unit) if v.second_unit else '')) if v.second_num else v.second) -%}
{#- pattern 'Glance', version 'with a word': the word steps down the hero ladder when it is longer than the layout was fitted on, and a
     status of several words that doesn't fit one line breaks over two; flagged, the hero block is the chip; a number as the
     state is drawn as any status (*Room sign*, *A number as the state*); only measured characters (*Glance with a word*, *Only measured characters*) -#}
{%- macro MW(w) -%}{{ w | upper | list | select('in', HWR) | join | regex_replace(' {2,}', ' ') | trim }}{%- endmacro -%}
{%- set word = (MW(v.word) if v.word else '') or (MW(v.name) if v.word else '') -%}
{{- GLANCE(ns, ds_title, as_timestamp(now()), word if word else '—', ds_icon if word else '', false, hlevel=v.level if word else '', txt=second, step=true, wrap=true) -}}
"""
PAYLOADS = [PAYLOAD_MAIN]
