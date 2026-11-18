"""Tiles on the 2.7" portrait: 1 x 3 tiles (Tiles)."""
PAYLOAD_MAIN = r'''
{%- set right = STAMP_AT(ds_last_ts, ds_stale) | float -%}
{%- set tl = namespace(l=[]) -%}
{%- for t in ds_tiles -%}{%- set tl.l = tl.l + [{'icon': t.icon, 'value': READING(t.raw, t.unit) if t.ok else '—', 'label': t.label, 'ok': t.ok}] -%}{%- endfor -%}
{#- pattern 'Tiles': 1 x 3 -#}
{{- TILES(ns, header_title_display, right, tl.l, 1, 3, ds_stale, ds_unavail_msg) -}}
'''
PAYLOADS = [PAYLOAD_MAIN]
