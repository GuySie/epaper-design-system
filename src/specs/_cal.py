"""Shared by every layout that draws the date-grouped list (the calendar's, and the weather and calendar page's): its day
headers (TODAY · weekday day month) and the overflow text, from the blueprint's days and its page's texts."""
CALM = r'''
{#- CALHEADS: the days as the list draws them (cal.l: a header and its event lines per day) and the '+N more' text (cal.more) -#}
{%- macro CALHEADS(cal) -%}
{%- for d in days -%}
{%- set wd = weekday_short_map[weekday_lang][(now().date() + timedelta(days=loop.index0)).weekday()] -%}
{%- set mo = months_short_map[weekday_lang][(now().date() + timedelta(days=loop.index0)).month - 1] -%}
{%- set cal.l = cal.l + [{'head': ((language_map[weekday_lang]['today'] ~ ' · ') if d.is_today else '') ~ wd ~ ' ' ~ d.day_num ~ ' ' ~ mo, 'lines': d.event_lines}] -%}
{%- endfor -%}
{%- set cal.more = language_map[weekday_lang]['more'] -%}
{%- endmacro -%}
'''
