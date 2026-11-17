ERR = r'''
{{- ERRPAGE(ns, (header_title if header_title else ds_wtxt['title']), ds_wtxt['nodata']) -}}
'''
STALE_TITLE = r'''
{%- set stale = (stale_after | int(0)) > 0 and wx.last > 0 and (as_timestamp(now()) - wx.last) > (stale_after | int(0)) * 60 -%}
{%- set right = wx.last if stale else as_timestamp(now()) -%}
'''
