import sys; sys.path.insert(0, __import__('os').path.dirname(__file__))
from _cal import CALM
PAYLOAD_MAIN = CALM + r'''
{%- set W, H, P, TH = EP_TK.width, EP_TK.height, EP_TK.space.pad, EP_TK.space.titleRow -%}
{#- pattern 'Grouped list': each day with its header (TODAY · weekday day month) and its event lines -#}
{%- set cal = namespace(l=[], more='') -%}{{- CALHEADS(cal) -}}
{{- GROUPED(ns, header_title_display, as_timestamp(now()), cal.l, cal.more, language_map[weekday_lang]['no_events']) -}}
'''

PAYLOAD_ERR = r'''
{{- ERRPAGE(ns, header_title_display, language_map[weekday_lang]['no_calendars']) -}}
'''
PAYLOADS = [PAYLOAD_MAIN, PAYLOAD_ERR]
