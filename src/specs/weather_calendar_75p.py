# Weather and calendar on the 7.5" portrait (design system: Hero dashboard with a chart or list, Weather and calendar): two equal
# halves. Top: the hero group (number, then the icon a hero gap after it) across the full width, the 7.5" detail rows a hero
# gap under it as a centred block as wide as the hero group for the widest reading; the alert row and the pollen row take
# pressure's place, then wind's, then high/low's (sunrise and sunset never make way); centred by ink between the title line
# and the divider. Bottom: the date-grouped list, its first text S below the divider. An error statement in the half whose
# data is missing. The hero is the layout's type.heroShared.
import sys; sys.path.insert(0, __import__('os').path.dirname(__file__))
from _wx import WX_TXT, WXM, ROWS_WIDE, ORDER_WIDE, LABELS_WIDE, VALUES_WIDE, HERO
from _wxerr import ERR, STALE_TITLE
from _cal import CALM
WX = True
CALENDAR = CALM + r'''
{#- the calendar half: the date-grouped list between top and bottom (the kit's DAYS), or the error statement in that half -#}
{%- macro CALENDAR(ns, top, bottom) -%}
{%- if calendar_entities | count == 0 -%}{{- ERRBLOCK(ns, language_map[weekday_lang]['no_calendars'], W, H, P, TH, top, bottom) -}}
{%- else -%}
{%- set cal = namespace(l=[], more='') -%}{{- CALHEADS(cal) -}}
{{- DAYS(ns, cal.l, P, W - P - 1, top, bottom, cal.more, language_map[weekday_lang]['no_events']) -}}
{%- endif -%}
{%- endmacro -%}
'''
PAYLOAD_MAIN = WXM + STALE_TITLE + CALENDAR + r'''
{%- set W, H, P, TH = EP_TK.width, EP_TK.height, EP_TK.space.pad, EP_TK.space.titleRow -%}
{%- set r = namespace(pol=none, wl=[], wv=[]) -%}{{- POLROW(r, ''' + LABELS_WIDE + r''', ''' + VALUES_WIDE + r''') -}}
{%- call(top, bottom) HERODASH(ns, (header_title if header_title else (ds_wtxt['title'] ~ ((' · ' ~ location_string) if location_string else ''))), right, stale,
     ''' + HERO + r''', ''' + ROWS_WIDE + r''', wx.flag, ''' + ORDER_WIDE + r''', r.wl, r.wv, r.pol, ''' + ORDER_WIDE + r''') -%}
{{- CALENDAR(ns, top, bottom) -}}
{%- endcall -%}
'''
# the error view has no weather model: the title without the stale part, as every weather error view
PAYLOAD_ERR = CALENDAR + r'''
{%- set W, H, P, TH = EP_TK.width, EP_TK.height, EP_TK.space.pad, EP_TK.space.titleRow -%}
{{- TITLE(ns, (header_title if header_title else ds_wtxt['title']), as_timestamp(now()), W, P, TH) -}}
{%- set ym = (P + TH + H - P) // 2 -%}
{{- ERRBLOCK(ns, ds_wtxt['nodata'], W, H, P, TH, P + TH + EP_TK.space.m, ym - EP_TK.space.m) -}}
{{- L(ns, P, ym, W - P - 1, ym) -}}
{{- CALENDAR(ns, ym + EP_TK.line.base + (SPACE_S(EP_TK.type.label[1]) | int), H - P) -}}
'''
PAYLOADS = [PAYLOAD_MAIN, PAYLOAD_ERR]
