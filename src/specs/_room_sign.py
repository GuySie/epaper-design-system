"""Room sign: one entity's state as a word, an optional second entity under it (Glance with a word). The drawing every screen shares."""
PAYLOAD_MAIN = r"""
{%- set v = ds_room -%}
{%- set second = ((NUMBER(v.second) ~ (('¦' ~ v.second_unit) if v.second_unit else '')) if v.second_num else v.second) -%}
{#- pattern 'Glance', version 'with a word': the word steps down the hero ladder when it is longer than the layout was fitted on, and a
     status of several words that doesn't fit one line breaks over two; flagged, it sits in the hero chip -#}
{{- GLANCE(ns, ds_title, as_timestamp(now()), (v.word | upper) if v.word else '—', ds_icon if v.word else '', false, hlevel=v.level, txt=second, step=true, wrap=true) -}}
"""
PAYLOADS = [PAYLOAD_MAIN]
