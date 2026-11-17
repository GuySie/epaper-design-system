import sys; sys.path.insert(0, __import__('os').path.dirname(__file__))
from _wx import WX_TXT, WXM, MOON_INPUT, TITLE_WIDE, ROWS_WIDE, ORDER_WIDE, LABELS_WIDE, VALUES_WIDE
from _wxerr import ERR, STALE_TITLE
WX = True
HOURS, DAYS = 6, 5      # the hour strip's and the day strip's cells (*Style choices*, Forecast horizon)
PAYLOAD_MAIN = WXM + STALE_TITLE + r'''
{%- set W, H, P, TH = EP_TK.width, EP_TK.height, EP_TK.space.pad, EP_TK.space.titleRow -%}
{#- Hero dashboard with forecast strips: bottom up the day strip, the hour strip, the hero band; the alert row and the pollen row take pressure's place, then wind's, then max/min's; sunrise and sunset never make way -#}
{{- WXDASH(ns, ''' + TITLE_WIDE + r''', right, stale,
     ''' + ROWS_WIDE + r''', ''' + ORDER_WIDE + r''',
     ''' + LABELS_WIDE + r''', ''' + VALUES_WIDE + r''', ''' + f'{HOURS}, {DAYS}' + r''', false, [2, 1, 5]) -}}
'''
PAYLOADS = [PAYLOAD_MAIN, ERR]
