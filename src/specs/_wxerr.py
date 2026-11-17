ERR = r'''
{%- set W, H, P, TH = EP_TK.width, EP_TK.height, EP_TK.space.pad, EP_TK.space.titleRow -%}
{{- TITLE(ns, (header_title if header_title else ds_wtxt['title']), as_timestamp(now()), W, P, TH) -}}
{{- ERRBLOCK(ns, ds_wtxt['nodata'], W, H, P, TH) -}}
'''
STALE_TITLE = r'''
{%- set stale = (stale_after | int(0)) > 0 and wx.last > 0 and (as_timestamp(now()) - wx.last) > (stale_after | int(0)) * 60 -%}
{%- set right = wx.last if stale else as_timestamp(now()) -%}
'''
