import sys; sys.path.insert(0, __import__('os').path.dirname(__file__))
from _wx import WX_TXT, WXM
from _wxerr import ERR, STALE_TITLE
WX = True
PAYLOAD_MAIN = WXM + STALE_TITLE + r'''
{%- set W, H, P, TH = EP_TK.width, EP_TK.height, EP_TK.space.pad, EP_TK.space.titleRow -%}
{#- Hero dashboard with forecast strips, portrait: the hero group over the forecast table -#}
{{- WXPORT(ns, (header_title if header_title else ds_wtxt['title']), right, stale, wind_or_precipitation == 'windspeed') -}}
'''
PAYLOADS = [PAYLOAD_MAIN, ERR]
