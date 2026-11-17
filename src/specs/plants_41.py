PAYLOAD_MAIN = r'''
{%- set W, H, P, TH = EP_TK.width, EP_TK.height, EP_TK.space.pad, EP_TK.space.titleRow -%}
{%- set right = (ds_last_ts | float(0)) if ds_stale else as_timestamp(now()) -%}
{%- set sev = severe_moisture_low | int(14) -%}
{%- set warn = warning_moisture_low | int(25) -%}
{#- the switch (*Thresholds*): off, no plant is flagged -#}
{%- if not (flag_moisture_low | default(true)) -%}{%- set sev, warn = -1, -1 -%}{%- endif -%}
{%- set it = namespace(l=[]) -%}
{%- for p in ds_plants -%}
{%- set val = ((p.pct | string) ~ '%') if p.ok else '—' -%}
{%- set kind = none if not p.ok else ('sev' if p.pct <= sev else ('warn' if p.pct <= warn else none)) -%}
{%- set it.l = it.l + [[p.label, val, kind]] -%}
{%- endfor -%}
{#- the footer's conclusion: how many plants need water, with the right plural (pl/hr have a few/many form) -#}
{%- set cnt = namespace(n=0) -%}{%- for p in ds_plants -%}{%- if p.ok and p.pct <= warn -%}{%- set cnt.n = cnt.n + 1 -%}{%- endif -%}{%- endfor -%}
{%- set wf = {'en': ['{n} plant needs water', '{n} plants need water'], 'nl': ['{n} plant water nodig', '{n} planten water nodig'],
     'de': ['{n} Pflanze braucht Wasser', '{n} Pflanzen brauchen Wasser'], 'fr': ['{n} plante à arroser', '{n} plantes à arroser'],
     'es': ['{n} planta necesita agua', '{n} plantas necesitan agua'], 'sv': ['{n} växt behöver vatten', '{n} växter behöver vatten'],
     'pl': ['{n} roślina potrzebuje wody', '{n} rośliny potrzebują wody', '{n} roślin potrzebuje wody'],
     'hr': ['{n} biljka treba vodu', '{n} biljke trebaju vodu', '{n} biljaka treba vodu']} -%}
{%- set wl = wf[weekday_lang] if weekday_lang in wf else wf['en'] -%}
{%- set nn = cnt.n | int -%}
{%- set wi = 0 if nn == 1 else ((1 if (nn % 10 in [2, 3, 4] and nn % 100 not in [12, 13, 14]) else 2) if wl | length == 3 else 1) -%}
{%- set wt = wl[wi] -%}
{%- set foot = (wt | replace('{n}', cnt.n | string) | upper) if cnt.n > 0 else '' -%}
{%- set unav = {'en': 'Most values unavailable.', 'de': 'Die meisten Werte nicht verfügbar.', 'nl': 'Meeste waarden niet beschikbaar.',
     'fr': 'La plupart des valeurs indisponibles.', 'es': 'La mayoría de los valores no disponibles.',
     'pl': 'Większość wartości niedostępna.', 'hr': 'Većina vrijednosti nedostupna.', 'sv': 'De flesta värden otillgängliga.'}.get(weekday_lang, 'Most values unavailable.') -%}
{#- pattern 'Key-value list', dense rows; the error state when most values are unavailable -#}
{{- KVPAGE(ns, header_title_display, right, it.l, ds_stale, ds_plants | rejectattr('ok') | list | length, unav, true, foot) -}}
'''

PAYLOAD_ERR = r'''
{{- ERRPAGE(ns, header_title_display, language_map[weekday_lang]['no_plants']) -}}
'''
PAYLOADS = [PAYLOAD_MAIN, PAYLOAD_ERR]
