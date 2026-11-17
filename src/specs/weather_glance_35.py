import sys; sys.path.insert(0, __import__('os').path.dirname(__file__))
from _wx import WX_TXT, WXM, GLANCE2, MOON_INPUT
from _wxerr import ERR, STALE_TITLE
WX = True
PAYLOAD_MAIN = WXM + STALE_TITLE + GLANCE2 + r'''
{%- set W, H, P, TH = EP_TK.width, EP_TK.height, EP_TK.space.pad, EP_TK.space.titleRow -%}
{%- call(y) GLANCE(ns, (header_title if header_title else ds_wtxt['title']), right, (wx.temp | string) ~ '°', wx.icon, stale, wx.temp_k, true, 'caller') -%}
{{- SECOND(ns, W // 2, y, FONT[EP_TK.type.secondary[0]], EP_TK.type.secondary[1], 0, W - 2 * P) -}}
{%- endcall -%}
'''
PAYLOADS = [PAYLOAD_MAIN, ERR]
