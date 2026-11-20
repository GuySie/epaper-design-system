"""Tiles: any entities as tiles, each its icon, state and label (Tiles). The drawing every screen shares; a layout names its
grid (COLS, ROWS: the most tiles its screen holds, *Tiles*)."""


def payloads(cols, rows):
    return [r'''
{%- set right = STAMP_AT(ds_last_ts, ds_stale) | float -%}
{%- set tl = namespace(l=[]) -%}
{%- for t in ds_tiles -%}{%- set tl.l = tl.l + [{'icon': t.icon, 'value': READING(t.raw, t.unit) if t.ok else '—', 'label': t.label, 'ok': t.ok}] -%}{%- endfor -%}
{#- pattern 'Tiles': the screen's grid -#}
{{- TILES(ns, header_title_display, right, tl.l, ''' + f'{cols}, {rows}' + r''', ds_stale, ds_unavail_msg) -}}
''']
