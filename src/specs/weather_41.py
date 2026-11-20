import sys; sys.path.insert(0, __import__('os').path.dirname(__file__))
from _wx import WX_TXT, WXM
from _wxerr import ERR, STALE_TITLE
WX = True
HOURS, DAYS = 4, 5      # the hour strip's and the day strip's cells (*Style choices*, Forecast horizon)
ROW_NAMES, ORDER = ('rain', 'wind', 'hum'), [2, 1, 0]      # the detail rows by name, and the order in which they make way for the alert row and the pollen row (*Override order*; the design system prints it from here)
PAYLOAD_MAIN = WXM + STALE_TITLE + r'''
{%- set W, H, P, TH = EP_TK.width, EP_TK.height, EP_TK.space.pad, EP_TK.space.titleRow -%}
{#- Hero dashboard with forecast strips: bottom up the footer, the day strip, the hour strip, the hero band; the alert row and the pollen row each take a row's place: humidity, wind, rain -#}
{{- WXDASH(ns, (header_title if header_title else ds_wtxt['title']), right, stale,
     [[ds_wtxt['rain'], MM(wx.mm_today), wx.mm_today_k], [ds_wtxt['wind'], WIND(), wx.wind_k], [ds_wtxt['hum'], ((wx.hum | string) ~ '%') if wx.hum is not none else '—', false]], ''' + str(ORDER) + r''',
     [ds_wtxt['rain'], ds_wtxt['wind'], ds_wtxt['hum']], [MM(99), MM(9.9), DECIMAL(100) ~ '¦' ~ wx.wind_unit, '100%'], ''' + f'{HOURS}, {DAYS}' + r''', true, ''' + str(ORDER) + r''') -}}
'''
PAYLOADS = [PAYLOAD_MAIN, ERR]
