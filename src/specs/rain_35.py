BARS, TICK_EVERY = 24, 6     # 5-minute bars over two hours; a tick every 30 minutes (*Style choices*, Axis ticks)
TICKS = '[' + ', '.join(f'[{i}, CLOCK(buckets[{i}].ts, h12, true)]' for i in range(0, BARS, TICK_EVERY)) + ']'
PAYLOAD_MAIN = r'''
{#- the rain chart fills its tier's canvas: 384 x 184 (3.5"), or 384 x 168 on the 2.7" (specs/rain_27l.py) -#}
{%- set W, H, P, TH = EP_TK.width, EP_TK.height, EP_TK.space.pad, EP_TK.space.titleRow -%}
{%- set h12 = time_format != '24h' -%}
{%- set right = (ds_last_ts | float(0)) if ds_stale else as_timestamp(now()) -%}
{%- set warn = warning_rain_hour | float(2.5) -%}
{%- set sev = severe_rain_hour | float(10) -%}
{#- the switch off: no bar is flagged, no threshold is drawn, the footer states the rain without a chip -#}
{%- set flag = flag_rain_hour | default(true) -%}
{#- the bars, the threshold lines with their labels, and the footer's conclusion in clock times -#}
{%- set bl = namespace(l=[]) -%}
{%- for b in buckets -%}{%- set bl.l = bl.l + [{'i': b.index, 'v': b.mm_h, 'f': b.scaled, 'level': ('sev' if b.is_severe else ('warn' if b.mm_h >= warn else '')) if flag else ''}] -%}{%- endfor -%}
{%- set lines = [[warn, DECIMAL((warn | round(1) | string).replace('.0', ''))], [sev, DECIMAL((sev | round(1) | string).replace('.0', ''))]] -%}
{%- set st = namespace(first=none, last=none, peak=0, peak_ts=0, sev_first=none, sev_last=none) -%}
{%- for b in buckets -%}{%- if b.mm_h > 0 -%}
{%- if st.first is none -%}{%- set st.first = b.ts -%}{%- endif -%}
{%- set st.last = b.ts -%}
{%- if b.mm_h > st.peak -%}{%- set st.peak, st.peak_ts = b.mm_h, b.ts -%}{%- endif -%}
{%- if b.is_severe -%}{%- if st.sev_first is none -%}{%- set st.sev_first = b.ts -%}{%- endif -%}{%- set st.sev_last = b.ts -%}{%- endif -%}
{%- endif -%}{%- endfor -%}
{%- set u = ds_txt['unit'] -%}
{%- set pk = DECIMAL((st.peak | round(0 if st.peak >= 10 else 1) | string).replace('.0', '')) ~ '¦' ~ u -%}
{%- if flag and st.sev_first is not none -%}
{%- set foot = [(ds_txt['heavy'] | upper) ~ ' ' ~ CLOCK_SPAN(st.sev_first, st.sev_last + 300, h12), (ds_txt['peak'] | upper) ~ ' ' ~ pk, 'sev'] -%}
{%- elif st.first is not none -%}
{%- set foot = [(ds_txt['rain'] | upper) ~ ' ' ~ CLOCK_SPAN(st.first, st.last + 300, h12), (ds_txt['peak'] | upper) ~ ' ' ~ pk ~ '¦ · ' ~ CLOCK(st.peak_ts, h12), none] -%}
{%- else -%}{%- set foot = ['', '', none] -%}{%- endif -%}
{%- set ticks = ''' + TICKS + r''' -%}
{%- set endtxt = CLOCK(buckets[23].ts + 300, h12, true) -%}
{%- set dry = (ds_txt['dry'] | upper) ~ ' ' ~ CLOCK(buckets[23].ts + 300, h12) -%}
{#- pattern 'Bar chart' with thresholds: 24 five-minute bars on a log scale; a wet bar is at least 3 x line.base high -#}
{{- BARCHART(ns, ds_title, right, 24, bl.l, lines, ticks, endtxt, foot, dry, ds_stale, 50, 0, 3, flag) -}}
'''

PAYLOAD_ERR = r'''
{{- ERRPAGE(ns, ds_title, language_map[weekday_lang]['no_data']) -}}
'''

PAYLOADS = [PAYLOAD_MAIN, PAYLOAD_ERR]
