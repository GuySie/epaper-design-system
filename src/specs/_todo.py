"""To-do list: a to-do entity's items as checkbox rows (Checklist). The drawing every screen shares."""
PAYLOAD_MAIN = r"""
{%- set tx = language_map[weekday_lang] -%}
{%- set wd = EP_DAYS_SHORT[weekday_lang] if weekday_lang in EP_DAYS_SHORT else EP_DAYS_SHORT['en'] -%}
{%- set mo = EP_MONTHS_SHORT[weekday_lang] if weekday_lang in EP_MONTHS_SHORT else EP_MONTHS_SHORT['en'] -%}
{%- set o = namespace(l=[]) -%}{%- set d = namespace(l=[]) -%}
{#- the due day: today's word, the weekday within six days either way, else the day and the month -#}
{%- for it in ds_todo.open -%}
{%- set n = it.n -%}
{%- set due = '' if n == '' else ((tx['today'] | upper) if n == 0 else ((wd[it.wd] | upper) if (n | abs) <= 6 else (it.day ~ ' ' ~ (mo[it.mon - 1] | upper)))) -%}
{%- set o.l = o.l + [{'text': it.s | string, 'due': due, 'level': it.lv}] -%}
{%- endfor -%}
{%- for it in ds_todo.done -%}{%- set d.l = d.l + [{'text': it.s | string, 'due': '', 'level': ''}] -%}{%- endfor -%}
{%- set short = ds_todo.n_open ~ ' ' ~ (tx['open'] | upper) -%}
{%- set foot = (short ~ ' · ' ~ ds_todo.n_done ~ ' ' ~ (tx['done'] | upper)) if ds_todo.counted else short -%}
{#- pattern 'Checklist' -#}
{{- CHECKLIST(ns, ds_title, as_timestamp(now()), o.l, d.l, foot, short, tx['more'], tx['nothing']) -}}
"""
PAYLOAD_ERR = r"""
{{- ERRPAGE(ns, ds_title, language_map[weekday_lang]['list_unavailable']) -}}
"""
PAYLOADS = [PAYLOAD_MAIN, PAYLOAD_ERR]
