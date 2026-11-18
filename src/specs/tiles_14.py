"""Tiles on the 1.4": one tile (Tiles)."""
PAYLOAD_MAIN = r'''
{%- set right = STAMP_AT(ds_last_ts, ds_stale) | float -%}
{%- set tl = namespace(l=[]) -%}
{%- for t in ds_tiles -%}{%- set tl.l = tl.l + [{'icon': t.icon, 'value': READING(t.raw, t.unit) if t.ok else '—', 'label': t.label, 'ok': t.ok}] -%}{%- endfor -%}
{#- pattern 'Tiles': one tile -#}
{{- TILES(ns, header_title_display, right, tl.l, 1, 1, ds_stale, ds_unavail_msg) -}}
'''
PAYLOADS = [PAYLOAD_MAIN]
