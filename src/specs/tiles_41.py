"""Tiles on the 4.1": 3 x 2 tiles (Tiles)."""
PAYLOAD_MAIN = r'''
{%- set right = STAMP_AT(ds_last_ts, ds_stale) | float -%}
{%- set tl = namespace(l=[]) -%}
{%- for t in ds_tiles -%}{%- set tl.l = tl.l + [{'icon': t.icon, 'value': READING(t.raw, t.unit) if t.ok else '—', 'label': t.label, 'ok': t.ok}] -%}{%- endfor -%}
{#- pattern 'Tiles': 3 x 2 -#}
{{- TILES(ns, header_title_display, right, tl.l, 3, 2, ds_stale, ds_unavail_msg) -}}
'''
PAYLOADS = [PAYLOAD_MAIN]
