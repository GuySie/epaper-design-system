"""The rain chart, shared by the two rain pages: a Bar chart with thresholds on the log scale of the rain intensity.

A page's data gives `buckets`, one per bar (`index`, `ts`: the bar's start, `mm_h`, `scaled`: its place on the scale);
its layout says how long a bar lasts and whether the chart's end is a day away (*Text rules*, *Dates in captions*)."""
from _defaults import default
BARS, TICK_EVERY = 24, 6     # the bars of the chart; a tick every sixth bar and at the end (*Style choices*, Axis ticks)
SCALE_TOP = 50               # mm/h: the top of the logarithmic scale, violent rain (*Chart frame (all charts)*, *Fixed y-scale*)
# the page's data follows the chart: as many buckets as bars, each scaled against the same top
VARIABLES = {'rain_bars': BARS, 'rain_top': SCALE_TOP}
TICKS = '[' + ', '.join(f'[{i}, CLOCK(buckets[{i}].ts, h12, true)]' for i in range(0, BARS, TICK_EVERY)) + ']'
ERR = r'''
{{- ERRPAGE(ns, ds_title, language_map[weekday_lang]['no_data']) -}}
'''


def payloads(page, bar_s, day_away=False):
    """the chart and the error page for `page`, whose bars last `bar_s` seconds; `day_away`: the dry statement names
    the end of the chart with its weekday"""
    main = r'''
{#- the rain chart fills its tier's canvas: 384 x 184 (3.5"), or 384 x 168 on the 2.7" -#}
{%- set W, H, P, TH = EP_TK.width, EP_TK.height, EP_TK.space.pad, EP_TK.space.titleRow -%}
{%- set h12 = time_format != '24h' -%}
{%- set right = STAMP_AT(ds_last_ts, ds_stale) | float -%}
{%- set warn = warning_rain_hour | float(''' + str(default(page, 'warning_rain_hour')) + r''') -%}
{%- set sev = severe_rain_hour | float(''' + str(default(page, 'severe_rain_hour')) + r''') -%}
{#- the switch off: no bar is flagged, no threshold is drawn, the footer states the rain without a chip -#}
{%- set flag = flag_rain_hour | default(true) -%}
{#- the bars, the threshold lines with their labels, and the footer's conclusion in clock times -#}
{%- set bl = namespace(l=[]) -%}
{%- for b in buckets -%}{%- set bl.l = bl.l + [{'i': b.index, 'v': b.mm_h, 'f': b.scaled, 'level': ('sev' if b.mm_h >= sev else ('warn' if b.mm_h >= warn else '')) if flag else ''}] -%}{%- endfor -%}
{%- set lines = [[warn, DECIMAL((warn | round(1) | string).replace('.0', ''))], [sev, DECIMAL((sev | round(1) | string).replace('.0', ''))]] -%}
{%- set st = namespace(first=none, last=none, peak=0, peak_ts=0, sev_first=none, sev_last=none) -%}
{%- for b in buckets -%}{%- if b.mm_h > 0 -%}
{%- if st.first is none -%}{%- set st.first = b.ts -%}{%- endif -%}
{%- set st.last = b.ts -%}
{%- if b.mm_h > st.peak -%}{%- set st.peak, st.peak_ts = b.mm_h, b.ts -%}{%- endif -%}
{%- if b.mm_h >= sev -%}{%- if st.sev_first is none -%}{%- set st.sev_first = b.ts -%}{%- endif -%}{%- set st.sev_last = b.ts -%}{%- endif -%}
{%- endif -%}{%- endfor -%}
{%- set u = ds_txt['unit'] -%}
{%- set pk = DECIMAL((st.peak | round(0 if st.peak >= 10 else 1) | string).replace('.0', '')) ~ '¦' ~ u -%}
{%- if flag and st.sev_first is not none -%}
{%- set foot = [(ds_txt['heavy'] | upper) ~ ' ' ~ CLOCK_SPAN(st.sev_first, st.sev_last + ''' + str(bar_s) + r''', h12), (ds_txt['peak'] | upper) ~ ' ' ~ pk, 'sev'] -%}
{%- elif st.first is not none -%}
{%- set foot = [(ds_txt['rain'] | upper) ~ ' ' ~ CLOCK_SPAN(st.first, st.last + ''' + str(bar_s) + r''', h12), (ds_txt['peak'] | upper) ~ ' ' ~ pk ~ '¦ · ' ~ CLOCK(st.peak_ts, h12), none] -%}
{%- else -%}{%- set foot = ['', '', none] -%}{%- endif -%}
{%- set ticks = ''' + TICKS + r''' -%}
{%- set endtxt = CLOCK(buckets[''' + str(BARS - 1) + r'''].ts + ''' + str(bar_s) + r''', h12, true) -%}
{%- set dry = (ds_txt['dry'] | upper) ~ ' ' ~ ''' + (f'STAMP(buckets[{BARS - 1}].ts + {bar_s})' if day_away else f'CLOCK(buckets[{BARS - 1}].ts + {bar_s}, h12)') + r''' -%}
{#- pattern 'Bar chart' with thresholds: BARS bars on a log scale up to SCALE_TOP; a wet bar is at least 3 x line.base high -#}
{{- BARCHART(ns, ds_title, right, ''' + str(BARS) + r''', bl.l, lines, ticks, endtxt, foot, dry, ds_stale, ''' + str(SCALE_TOP) + r''', 0, 3, flag) -}}
'''
    return [main, ERR]
