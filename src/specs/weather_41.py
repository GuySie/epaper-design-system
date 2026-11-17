import sys; sys.path.insert(0, __import__('os').path.dirname(__file__))
from _wx import WX_TXT, WXM
from _wxerr import ERR, STALE_TITLE
WX = True
HOURS, DAYS = 4, 5      # the hour strip's and the day strip's cells (*Style choices*, Forecast horizon)
PAYLOAD_MAIN = WXM + STALE_TITLE + r'''
{%- set W, H, P, TH = EP_TK.width, EP_TK.height, EP_TK.space.pad, EP_TK.space.titleRow -%}
{#- Hero dashboard with forecast strips: bottom up the footer, the day strip, the hour strip, the hero band; the alert row and the pollen row each take a row's place: humidity, wind, rain -#}
{{- WXDASH(ns, (header_title if header_title else ds_wtxt['title']), right, stale,
     [[ds_wtxt['rain'], MM(wx.mm_today), wx.mm_today_k], [ds_wtxt['wind'], WIND(), wx.wind_k], [ds_wtxt['hum'], ((wx.hum | string) ~ '%') if wx.hum is not none else '—', false]], [2, 1, 0],
     [ds_wtxt['rain'], ds_wtxt['wind'], ds_wtxt['hum']], [MM(99), MM(9.9), DECIMAL(100) ~ '¦' ~ wx.wind_unit, '100%'], ''' + f'{HOURS}, {DAYS}' + r''', true, [2, 1, 0]) -}}
'''
PAYLOADS = [PAYLOAD_MAIN, ERR]
