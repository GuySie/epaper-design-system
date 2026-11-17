import sys; sys.path.insert(0, __import__('os').path.dirname(__file__))
from _wx import WXM
PAYLOAD_MAIN = WXM + r'''
{%- set W, H, P, TH = EP_TK.width, EP_TK.height, EP_TK.space.pad, EP_TK.space.titleRow -%}
{%- set title = header_title if header_title else ds_otxt['title'] -%}
{%- set items = ds_open['items'] -%}
{%- set n = items | count -%}
{%- set icon = 'mdi:home-lock' if n == 0 else ('mdi:window-open' if items[0].win else 'mdi:door-open') -%}
{%- if n == 0 -%}
{{- GLANCE(ns, title, as_timestamp(now()), n | string, icon, txt=ds_otxt['all'] | upper) -}}
{%- else -%}
{#- the first open one names the chip (severe ones first); "+N" for the rest. Too wide: the area alone, then cut -#}
{%- set kind = 'sev' if ds_open['sev'] > 0 else 'warn' -%}
{%- set more = (' +' ~ (n - 1)) if n > 1 else '' -%}
{%- set full = LEVEL_MARK(kind) ~ (items[0].label | upper) ~ more -%}
{%- set short = LEVEL_MARK(kind) ~ (items[0].area | upper) ~ more -%}
{%- set sf, ss = FONT[EP_TK.type.secondary[0]], EP_TK.type.secondary[1] -%}
{#- a chip is the text + 2 x space.s wide (less the 2 px trailing bearing) -#}
{%- set v = full if (VALUE_W(full, ss, sf) | int) + 2 * (SPACE_S(ss) | int) - 2 <= W - 2 * P else short -%}
{{- GLANCE(ns, title, as_timestamp(now()), n | string, icon, sec='chip', txt=v, llevel=kind) -}}
{%- endif -%}
'''
PAYLOAD_ERR = r'''
{{- ERRPAGE(ns, (header_title if header_title else ds_otxt['title']), ds_otxt['none']) -}}
'''
PAYLOADS = [PAYLOAD_MAIN, PAYLOAD_ERR]
