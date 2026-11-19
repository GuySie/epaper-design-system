"""The price chart: a Bar chart for prices, the hours of today (*Bar chart for prices*).

A page's data gives `hours`, one per bar (`index`, `ts`: the hour's start, `ct`: its price in whole cents, none without
a price), or an empty list when no hour has a price (the error view)."""
from _defaults import default
BARS, TICK_EVERY = 24, 6     # the bars of the chart; a tick every sixth bar and at the end (*Style choices*, Axis ticks)
SCALE_STEP = 10              # a scale that goes under zero ends on a whole 10 (*Bar chart for prices*, Scale)
WIDEST = '-10'               # the label the margin is sized for
# the page's data follows the chart: as many hours as bars
VARIABLES = {'price_bars': BARS}
TICKS = '[' + ', '.join(f'[{i}, CLOCK(hours[{i}].ts, h12, true)]' for i in range(0, BARS, TICK_EVERY)) + ']'
ERR = r'''
{{- ERRPAGE(ns, ds_title, language_map[weekday_lang]['no_data']) -}}
'''


def payloads(page):
    """the chart and the error page for `page`"""
    main = r'''
{%- set h12 = time_format != '24h' -%}
{%- set warn = warning_price | float(''' + str(default(page, 'warning_price')) + r''') -%}
{%- set sev = severe_price | float(''' + str(default(page, 'severe_price')) + r''') -%}
{%- set run = [cheapest_hours | int(''' + str(default(page, 'cheapest_hours')) + r'''), 1] | max -%}
{#- the switch off: no bar is flagged, no threshold is drawn, the footer states its facts without a chip -#}
{%- set flag = flag_price | default(true) -%}
{%- set n = ''' + str(BARS) + r''' -%}
{%- set cur = [[((as_timestamp(now()) - hours[0].ts) // 3600) | int, 0] | max, n - 1] | min -%}
{%- set known = hours | rejectattr('ct', 'none') | list -%}
{#- the scale: 0 up to the top of a chart with thresholds; under zero on a day with a negative price -#}
{%- set top = [EP_CHART.top * sev, 1] | max -%}
{%- set lowest = known | map(attribute='ct') | min -%}
{%- set bot = 0 if lowest >= 0 else ((lowest / ''' + str(SCALE_STEP) + r''') | round(0, 'floor') * ''' + str(SCALE_STEP) + r''') | int -%}
{#- the bars: an hour gone is outlined; the current hour and the hours to come carry their level -#}
{%- set bl = namespace(l=[]) -%}
{%- for h in known -%}
{%- set gone = h.index < cur -%}
{%- set bl.l = bl.l + [{'i': h.index, 'v': h.ct, 'f': ([h.ct, top] | min) / (top - bot), 'out': gone, 'level': ('sev' if h.ct >= sev else ('warn' if h.ct >= warn else '')) if (flag and not gone) else ''}] -%}
{%- endfor -%}
{%- set lines = [[warn, DECIMAL((warn | round(1) | string).replace('.0', ''))], [sev, DECIMAL((sev | round(1) | string).replace('.0', ''))]] -%}
{#- the footer: the current price, and the cheapest run of hours still to come -#}
{%- set u = ds_txt['unit'] -%}
{%- set nowp = hours[cur].ct -%}
{%- set best = namespace(i=none, s=0) -%}
{%- for i in range(cur, n - run + 1) -%}{%- set w = hours[i:i + run] | map(attribute='ct') | reject('none') | list -%}
{%- if (w | length) == run and (best.i is none or (w | sum) < best.s) -%}{%- set best.i, best.s = i, w | sum -%}{%- endif -%}{%- endfor -%}
{%- set foot = [((ds_txt['now'] | upper) ~ ' ' ~ nowp ~ '¦' ~ u) if nowp is not none else '',
                ((ds_txt['cheapest'] | upper) ~ ' ' ~ CLOCK_SPAN(hours[best.i].ts, hours[best.i].ts + run * 3600, h12)) if best.i is not none else '',
                (('sev' if nowp >= sev else ('warn' if nowp >= warn else none)) if (flag and nowp is not none) else none)] -%}
{%- set ticks = ''' + TICKS + r''' -%}
{%- set endtxt = CLOCK(hours[n - 1].ts + 3600, h12, true) -%}
{#- pattern 'Bar chart' for prices: BARS bars on the scale with thresholds; a bar is at least 3 x line.base high -#}
{{- BARCHART(ns, ds_title, as_timestamp(now()), n, bl.l, lines, ticks, endtxt, foot, '', false, 0, top, 3, flag,
             {'signed': true, 'lo': bot, 'lolabel': bot | string, 'widest': ''' + repr(WIDEST) + r''', 'tail': ds_txt['none']}) -}}
'''
    return [main, ERR]
