"""Bin day: the bin collected next as a word, the day under it (Glance with a word). The drawing every screen shares."""
PAYLOAD_MAIN = r"""
{%- set tx = language_map[weekday_lang] -%}
{%- set wd = EP_DAYS_SHORT[weekday_lang] if weekday_lang in EP_DAYS_SHORT else EP_DAYS_SHORT['en'] -%}
{%- set mo = EP_MONTHS_SHORT[weekday_lang] if weekday_lang in EP_MONTHS_SHORT else EP_MONTHS_SHORT['en'] -%}
{%- set right = as_timestamp(now()) -%}
{%- set first = ds_bins[0] -%}
{%- set same = ds_bins | selectattr('d', 'eq', first.d) | list -%}
{%- set when = (tx['today'] | upper) if first.d == 0 else ((tx['tomorrow'] | upper) if first.d == 1 else ((wd[first.wd] | upper) ~ ' ' ~ first.day ~ ' ' ~ (mo[first.mon - 1] | upper))) -%}
{%- set lvl = ('sev' if first.d == 0 else ('warn' if first.d == 1 else '')) if flag_soon else '' -%}
{%- set when = when ~ ((' · +' ~ ((same | length) - 2)) if (same | length) > 2 else '') -%}
{#- pattern 'Glance', version 'with a word': the word steps down the hero ladder when it is longer than the layout was fitted
     on; two bins on one day stack (hero2) -#}
{{- GLANCE(ns, header_title_display, right, first.word | upper, first.icon, false, sec=('chip' if lvl else 'text'), txt=when, llevel=lvl, step=true, wrap=true,
     hero2=((same[1].word | upper) if (same | length) > 1 else '')) -}}
"""
PAYLOAD_ERR = r"""
{{- ERRPAGE(ns, header_title_display, language_map[weekday_lang]['no_dates']) -}}
"""
PAYLOADS = [PAYLOAD_MAIN, PAYLOAD_ERR]
