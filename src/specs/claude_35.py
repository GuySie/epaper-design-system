PAYLOAD_MAIN = r'''
{%- set W, H, P, TH = EP_TK.width, EP_TK.height, EP_TK.space.pad, EP_TK.space.titleRow -%}
{%- set right = STAMP_AT(ds_last_ts, ds_stale) | float -%}
{%- set n = bars | length -%}
{#- drop the words every bar label shares, so the part that differs is visible -#}
{%- set labs = bars | map(attribute='label') | map('string') | list -%}
{%- set cp = namespace(pre='', go=n > 1) -%}
{%- if n > 1 -%}{%- for w in labs[0].split(' ')[:-1] -%}
{%- set cand = cp.pre ~ w ~ ' ' -%}
{%- set hit = namespace(c=0) -%}{%- for l in labs -%}{%- if l[:cand | length] == cand -%}{%- set hit.c = hit.c + 1 -%}{%- endif -%}{%- endfor -%}
{%- if cp.go and hit.c == n -%}{%- set cp.pre = cand -%}{%- else -%}{%- set cp.go = false -%}{%- endif -%}
{%- endfor -%}{%- endif -%}
{#- reset caption: RESET + clock time within 24 h, else RESET + weekday + time (interface word uppercase, dates as in the stamp) -#}
{%- macro RCAP(b) -%}{%- set rts = b.reset_ts | float(0) -%}{{ ((language_map[weekday_lang]['resets_prefix'] | upper) ~ ' ' ~ ((rts | timestamp_custom('%H:%M' if time_format == '24h' else '%-I:%M %p')) if (rts - as_timestamp(now())) < 86400 else STAMP(rts))) if rts > 0 else '' }}{%- endmacro -%}
{#- the bars as the pattern draws them: labels without the shared words, the reset caption written out -#}
{%- set bl = namespace(l=[]) -%}
{%- for b in bars -%}
{%- set bl.l = bl.l + [{'label': ((b.label | string)[cp.pre | length:] if cp.pre else b.label), 'percent': b.percent, 'percent_text': b.percent_text,
     'marker_pct': b.marker_pct, 'is_severe': b.is_severe, 'is_warning': b.is_warning, 'rcap': RCAP(b)}] -%}
{%- endfor -%}
{#- the footer's conclusion: on pace, or the bar furthest ahead of its period (warning) -#}
{%- set has_pace = (bars | selectattr('marker_pct', 'ne', none) | list | length) > 0 -%}
{%- set pace = namespace(d=-999, lab='') -%}
{%- for b in bars -%}{%- if b.marker_pct is not none and b.percent_text != '--' -%}{%- set d = b.percent - b.marker_pct -%}
{%- if d > pace.d -%}{%- set pace.d, pace.lab = d, ((b.label | string)[cp.pre | length:] if cp.pre else b.label) -%}{%- endif -%}{%- endif -%}{%- endfor -%}
{%- set pt = {'en': ['ON PACE', '{l} {d}% AHEAD'], 'de': ['IM PLAN', '{l} {d}% VORAUS'], 'nl': ['OP SCHEMA', '{l} {d}% VOOR'], 'fr': ['DANS LES TEMPS', "{l} {d}% D'AVANCE"], 'es': ['A TIEMPO', '{l} {d}% ADELANTADO'], 'pl': ['W NORMIE', '{l} {d}% PONAD'], 'hr': ['U ROKU', '{l} {d}% IZNAD'], 'sv': ['I FAS', '{l} {d}% FÖRE']}.get(weekday_lang, ['ON PACE', '{l} {d}% AHEAD']) -%}
{%- set foot = '' if pace.d == -999 else ((pt[1] | replace('{l}', pace.lab | upper) | replace('{d}', pace.d | round | int | string)) if pace.d > 0 else pt[0]) -%}
{#- pattern 'Meters' -#}
{{- METERS(ns, header_title_display, right, bl.l, ds_stale, has_pace, foot, 'warn' if (pace.d > 0 and (flag_usage | default(true))) else none) -}}
'''

PAYLOAD_ERR = r'''
{{- ERRPAGE(ns, header_title_display, language_map[weekday_lang]['no_bars']) -}}
'''
PAYLOADS = [PAYLOAD_MAIN, PAYLOAD_ERR]
