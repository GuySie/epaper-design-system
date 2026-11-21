"""Appliance run: when an appliance's run ends, the bar of how far it is, the programme under it (Glance with a progress bar).
The drawing every screen shares."""
import pathlib
import yaml
# the bar is as wide as the hero group of the page's widest reading (*Glance with a progress bar*), which the registry holds
WIDEST = yaml.safe_load((pathlib.Path(__file__).resolve().parent.parent / 'registry.yaml').read_text())['pages']['appliance']['widest']
PAYLOAD_MAIN = r"""
{%- set v = ds_run -%}
{%- set tx = language_map[weekday_lang] -%}
{%- set W, H, P, TH = EP_TK.width, EP_TK.height, EP_TK.space.pad, EP_TK.space.titleRow -%}
{#- follows *Appliance run* -#}
{%- if v.st == 'err' -%}{{- ERRPAGE(ns, ds_title, tx['unavailable']) -}}
{%- elif v.st == 'idle' -%}
{{- TITLE(ns, ds_title, as_timestamp(now()), W, P, TH) -}}
{{- EMPTY(ns, tx['idle'], P, W - P - 1, P + TH, H - P) -}}
{%- else -%}
{%- set h12 = time_format == '12h' -%}
{#- 12-hour time: the half of the day is the hero's unit (*Appliance run*, *12-hour time*) -#}
{%- set hero = ((v.end | timestamp_custom('%-I:%M' if h12 else '%H:%M')) if v.end is not none else '—') -%}
{%- set unit = ((v.end | timestamp_custom('%p') | lower) if (h12 and v.end is not none) else '') -%}
{%- set sf, ss = FONT[EP_TK.type.secondary[0]], EP_TK.type.secondary[1] -%}
{%- call(y) GLANCE(ns, ds_title, as_timestamp(now()), hero, ds_icon if v.end is not none else '', sec='caller', unit=unit, bar=v.share, blevel=v.level, bwide='@WIDEST@') -%}
{%- if v.level -%}
{#- flagged: the Glance secondary is the chip, its text cut where it doesn't fit between the paddings (the chip hangs into them) -#}
{%- set c = (tx['done'] ~ ' · ' ~ tx['closed']) | upper -%}
{{- CCHIP(ns, CUT(c, ss, sf, W - 2 * P), W // 2, y, sf, ss, 0, LEVEL_FILL(v.level), LEVEL_TEXT(v.level)) -}}
{%- elif v.st == 'done' -%}
{{- T(ns, tx['done'] | upper, W // 2, y, sf, ss, color.ink, 'mm', W - 2 * P) -}}
{%- else -%}
{#- the programme gives way: it is cut so the percentage stays whole (*Appliance run*, *A long programme*) -#}
{%- set tail = ((' · ' if v.prog else '') ~ v.pct ~ '%') if v.pct is not none else '' -%}
{%- set tw = (VALUE_W(tail, ss, sf) | int) if tail else 0 -%}
{#- follows *Text rules*, *Case: interface in capitals, content as written*: the programme is the user's data -#}
{%- set pg = CUT(v.prog, ss, sf, W - 2 * P - tw) if v.prog else '' -%}
{%- set pw = (VALUE_W(pg, ss, sf) | int) if pg else 0 -%}
{%- set x0 = ((W - pw - tw) / 2) | round | int -%}
{%- if pg -%}{{- T(ns, pg, x0, y, sf, ss, color.ink, 'lm') -}}{%- endif -%}
{%- if tail -%}{{- T(ns, tail, x0 + pw, y, sf, ss, color.ink, 'lm') -}}{%- endif -%}
{%- endif -%}
{%- endcall -%}
{%- endif -%}
""".replace('@WIDEST@', WIDEST)
PAYLOADS = [PAYLOAD_MAIN]
