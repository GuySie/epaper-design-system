PAYLOAD_MAIN = r'''
{%- set W, H, P, TH = EP_TK.width, EP_TK.height, EP_TK.space.pad, EP_TK.space.titleRow -%}
{#- the Glance: title row without a stamp (the hero time is the moment of the last press, which is also the last update),
     hero group (time, pill), and the press date as the Glance secondary -#}
{%- set is12 = ' AM' in press_time_label or ' PM' in press_time_label -%}
{#- overdue: severity takes the Glance secondary, the press date becomes a warning / severe chip -#}
{#- a warning / severe chip names its problem: the status word follows the date (OVERDUE at warning, MISSED at severe) -#}
{#- the date belongs to the hero time (the last dose), so it comes first; the status follows it -#}
{%- set otag = (' · ' ~ (language_map[weekday_lang]['missed' if ds_overdue_k == 'sev' else 'overdue'] | upper)) if ds_overdue_k else '' -%}
{%- set ampm = (' · ' ~ press_time_label[-2:]) if is12 else '' -%}
{%- set dtxt = LEVEL_MARK(ds_overdue_k) ~ (ds_date | upper) ~ ampm ~ otag -%}
{#- a chip that doesn't fit (wider than the paddings plus the S a chip hangs out on each side): the weekday gives way first (*Medication*, 12-hour time) -#}
{%- if ds_overdue_k and (CHIPW(dtxt, EP_TK.type.secondary[1], FONT[EP_TK.type.secondary[0]]) | int) > W - 2 * P + 2 * (SPACE_S(EP_TK.type.secondary[1]) | int) -%}
{%- set dtxt = LEVEL_MARK(ds_overdue_k) ~ ((ds_date | upper).split(' ', 1) | last) ~ ampm ~ otag -%}
{%- endif -%}
{{- GLANCE(ns, header_title_display, '', press_time_label | replace(' AM', '') | replace(' PM', ''), 'mdi:pill',
          sec=('chip' if ds_overdue_k else 'text'), txt=dtxt, llevel=ds_overdue_k, cut=false) -}}
'''
PAYLOADS = [PAYLOAD_MAIN]
