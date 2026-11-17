PAYLOAD_MAIN = r'''
{%- set W, H, P, TH = EP_TK.width, EP_TK.height, EP_TK.space.pad, EP_TK.space.titleRow -%}
{#- pattern 'Event list' (one event: the event hero); with fewer events the rows spread by one step -#}
{{- EVENTS(ns, header_title_display, as_timestamp(now()), events_data, language_map[weekday_lang]['until'], [language_map[weekday_lang]['free_until'], language_map[weekday_lang]['free_from']], language_map[weekday_lang]['today'], language_map[weekday_lang]['no_events']) -}}
'''

PAYLOAD_ERR = r'''
{%- set W, H, P, TH = EP_TK.width, EP_TK.height, EP_TK.space.pad, EP_TK.space.titleRow -%}
{{- TITLE(ns, header_title_display, as_timestamp(now()), W, P, TH) -}}
{{- ERRBLOCK(ns, language_map[weekday_lang]['no_calendars'], W, H, P, TH) -}}
'''
PAYLOADS = [PAYLOAD_MAIN, PAYLOAD_ERR]
