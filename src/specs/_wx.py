"""Shared pieces for the weather specs."""
import pathlib
WX_TXT = (pathlib.Path(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.dirname(__file__)), 'wx_txt.yaml'))).read_text()

STALE_VARS = '''  ds_stale: >-
    {{ false }}
'''

# the 7.5" detail rows (weather_75, weather_75p, weather_calendar_75p): rain, wind, pressure, sunrise, sunset, high/low; their labels and widest values
# (the detail column); the order in which the alert row and the pollen row take a row's place (pressure, wind, high/low;
# sunrise and sunset never make way)
TITLE_WIDE = r"""(header_title if header_title else (ds_wtxt['title'] ~ ((' · ' ~ location_string) if location_string else '')))"""
ROWS_WIDE = r"""[[ds_wtxt['rain'], MM(wx.mm_today), wx.mm_today_k], [ds_wtxt['wind'], WIND(), wx.wind_k], [ds_wtxt['pres_l'], ((wx.pres | string) ~ '¦' ~ wx.pres_unit) if wx.pres is not none else '—', false], [ds_wtxt['rise_l'], wx.rise, false], [ds_wtxt['set_l'], wx.set, false], [ds_wtxt['hilo'], wx.hi ~ '° / ' ~ wx.lo ~ '°', wx.hilo_k]]"""
LABELS_WIDE = r"""[ds_wtxt['rain'], ds_wtxt['wind'], ds_wtxt['pres_l'], ds_wtxt['rise_l'], ds_wtxt['set_l'], ds_wtxt['hilo']]"""
VALUES_WIDE = r"""[MM(99), MM(9.9), DECIMAL(100) ~ '¦' ~ wx.wind_unit, '1050¦' ~ wx.pres_unit, '12:00 PM' if time_format == '12h' else '00:00', '-10° / -15°']"""
ORDER_WIDE = '[2, 1, 5]'
# the weather's hero as the kit's hero group takes it (HERO_SHARED): the temperature, its flag, the condition icon with the moon
# badge, and the widest reading the page must show (registry.yaml: widest)
WIDEST = "'-12°'"
HERO = r"""{'text': (wx.temp | string) ~ '°', 'level': wx.temp_k, 'icon': wx.icon, 'moon': true, 'widest': """ + WIDEST + "}"
PORT_HOURS, PORT_DAYS = 3, 3     # the 2.7" portrait's forecast table: hour rows, and at most this many day rows (as many as fit); one more without pollen

# macros used by every weather layout (prepended to the payload body)
WXM = r'''
{%- macro MM(v) -%}{{ '0¦mm' if (v | float(0)) == 0 else (DECIMAL(((v | float) | round(0 if (v | float) >= 10 else 1) | string).replace('.0', '')) ~ '¦mm') }}{%- endmacro -%}
{#- the wind with its unit; a missing value is — alone (*Units and numbers*, *Missing values*) -#}
{%- macro WIND() -%}{{ '—' if wx.wind == '—' else (DECIMAL(wx.wind) ~ '¦' ~ wx.wind_unit) }}{%- endmacro -%}
{#- a value centred at cx: plain / warning chip / severe chip -#}
{%- macro CELL_VALUE(ns, v, cx, cy, f, fb, s, cw, k='', bold=true, p=0) -%}
{%- if k -%}{{- CCHIP(ns, LEVEL_MARK(k) ~ v, cx, cy, fb, s, cw, LEVEL_FILL(k), LEVEL_TEXT(k), p) -}}
{%- else -%}{{- T(ns, v, cx, cy, fb if bold else f, s, color.ink, 'mm') -}}{%- endif -%}
{%- endmacro -%}
{#- Strip cells (component 'Hour cell / Day cell'): every text line is type.data, the regular text lines (hour, high/low, a dry 0 mm)
     in its Regular cut where that cut's stems clear stroke.min (DATA_REGULAR), else Bold. A text line's box is rowMin of type.data
     (cap height + 2 x space.xs + 1); stacked items are space.xs apart, so text lines are space.detailRow apart and a chip on a text line is that pitch - 1 high (a 1 px paper gap to a chip next to it); an icon sits space.xs from the text lines around it. -#}
{%- macro CELL_ROW_H() -%}{%- set ds = EP_TK.type.data[1] -%}{{ (CAPH(ds) | int) + 2 * (SPACE_XS(ds) | int) + 1 }}{%- endmacro -%}
{#- CELLH: a cell's height: three text lines and, with an icon, the icon -#}
{%- macro CELLH(ic) -%}{%- set xs = SPACE_XS(EP_TK.type.data[1]) | int -%}{{ 3 * (CELL_ROW_H() | int) + 2 * xs + ((ic + xs) if ic else 0) }}{%- endmacro -%}
{#- hour cell: time / [icon] / temp / mm; y is the top of the cell -#}
{%- macro HCELL(ns, h, cx, y, ic) -%}
{%- set ds, df, rf = EP_TK.type.data[1], FONT[EP_TK.type.data[0]], DATA_REGULAR() -%}
{%- set xs, r = SPACE_XS(ds) | int, CELL_ROW_H() | int -%}{%- set p = r + xs -%}
{{- CELL_VALUE(ns, h.t, cx, y + xs + CAPUP[ds], rf, df, ds, 0, h.icon_k, false, 0 if ic else p) -}}
{%- set yy = y + r + xs -%}
{%- if ic -%}{{- I(ns, h.icon, cx, yy + ic // 2, ic) -}}{%- set yy = yy + ic + xs -%}{%- endif -%}
{{- CELL_VALUE(ns, (h.temp | string) ~ '°', cx, yy + xs + CAPUP[ds], rf, df, ds, 0, h.temp_k, true, p) -}}
{{- CELL_VALUE(ns, MM(h.mm), cx, yy + p + xs + CAPUP[ds], rf, df, ds, 0, h.mm_k, h.mm > 0, p) -}}
{%- endmacro -%}
{#- day cell: day / icon / hi/lo / mm -#}
{%- macro DCELL(ns, d, cx, y, ic) -%}
{%- set ds, df, rf = EP_TK.type.data[1], FONT[EP_TK.type.data[0]], DATA_REGULAR() -%}
{%- set xs, r = SPACE_XS(ds) | int, CELL_ROW_H() | int -%}{%- set p = r + xs -%}
{{- CELL_VALUE(ns, d.d | upper, cx, y + xs + CAPUP[ds], rf, df, ds, 0, d.icon_k) -}}
{%- set yy = y + r + xs -%}
{{- I(ns, d.icon, cx, yy + ic // 2, ic) -}}
{%- set yy = yy + ic + xs -%}
{{- CELL_VALUE(ns, (d.hi | string) ~ '°/' ~ (d.lo | string) ~ '°', cx, yy + xs + CAPUP[ds], rf, df, ds, 0, d.t_k, false, p) -}}
{{- CELL_VALUE(ns, MM(d.mm), cx, yy + p + xs + CAPUP[ds], rf, df, ds, 0, d.mm_k, d.mm > 0, p) -}}
{%- endmacro -%}
{#- Strips (a line, space.s, a row of cells). STRIPY: the line's y for a strip whose last text line's ink ends just above yb (the
     bottom of the content, the footer's M, or space.s above the next strip's line): the cells' box ends space.xs + 1 lower -#}
{%- macro STRIPY(yb, ic) -%}{{ yb + (SPACE_XS(EP_TK.type.data[1]) | int) + 1 - (CELLH(ic) | int) - (SPACE_S(EP_TK.type.data[1]) | int) - EP_TK.line.base }}{%- endmacro -%}
{#- HSTRIP: n equal cells of hours under the line at y -#}
{%- macro HSTRIP(ns, y, n, ic, W, P) -%}
{{- L(ns, P, y, W - P - 1, y) -}}
{%- set top, cw = y + EP_TK.line.base + (SPACE_S(EP_TK.type.data[1]) | int), (W - 2 * P) / n -%}
{%- set hrs = wx.hours[1:n + 1] if wx.hours | length > n else wx.hours[:n] -%}
{%- for h in hrs -%}{{- HCELL(ns, h, (P + cw * loop.index0 + cw / 2) | round | int, top, ic) -}}{%- endfor -%}
{%- endmacro -%}
{#- DSTRIP: n equal cells of days under the line at y -#}
{%- macro DSTRIP(ns, y, n, ic, W, P) -%}
{{- L(ns, P, y, W - P - 1, y) -}}
{%- set top, cw = y + EP_TK.line.base + (SPACE_S(EP_TK.type.data[1]) | int), (W - 2 * P) / n -%}
{%- for d in wx.days[:n] -%}{{- DCELL(ns, d, (P + cw * loop.index0 + cw / 2) | round | int, top, ic) -}}{%- endfor -%}
{%- endmacro -%}
{#- POLROW: the pollen row (r.pol: type, count and level while pollen is above 0, else none) and the detail column's labels
     and widest values with it (r.wl, r.wv: the configured type and a 3-digit count; a longer one cuts the type) -#}
{%- macro POLROW(r, wl, wv) -%}
{%- set p = wx.pollen -%}
{%- set r.pol = [p.name, p.v, p.k] if (p is not none and p.show) else none -%}
{%- set r.wl = (wl + [p.name]) if p is not none else wl -%}
{%- set r.wv = (wv + ['999' ~ (('¦' ~ (p.v | string).split('¦')[1]) if '¦' in (p.v | string) else '')]) if p is not none else wv -%}
{%- endmacro -%}
{#- the footer's chip: the most severe rain flag among today's total and the forecast hours; none when the whole forecast is dry -#}
{%- macro FOOT_LEVEL() -%}
{%- set ks = [wx.mm_today_k] + (wx.hours | map(attribute='mm_k') | list) -%}
{%- set wet = (wx.hours | selectattr('mm', 'gt', 0) | list | length) > 0 -%}
{{ ('sev' if 'sev' in ks else ('warn' if 'warn' in ks else '')) if wet else '' }}
{%- endmacro -%}
{#- forecast conclusion for a footer: dry until the first wet hour, rain until the first dry hour, or dry for the whole forecast -#}
{%- macro FOOT_FORECAST() -%}
{%- set hs = wx.hours -%}
{%- if not hs -%}{{ '' }}
{%- elif hs[0].mm > 0 -%}
{%- set nx = hs | selectattr('mm', 'le', 0) | list -%}
{{ ((ds_wtxt['rain_until'] | upper) ~ ' ' ~ nx[0].t) if nx else (ds_wtxt['rain'] | upper) }}
{%- else -%}
{%- set nx = hs | selectattr('mm', 'gt', 0) | list -%}
{{ ((ds_wtxt['dry_until'] | upper) ~ ' ' ~ nx[0].t) if nx else (ds_wtxt['dry'] | upper) }}
{%- endif -%}
{%- endmacro -%}
{#- the one flagged item for a single slot, in the system-wide order: an official warning; else the most severe of
     the current condition, pollen (if wp), today's rain, wind - on a tie in that order. Returns 'kind§label§value§short' or '' -#}
{%- macro PICK(wp=true) -%}
{%- set p = wx.pollen -%}
{%- set c = [] -%}
{%- if wx.flag and not wx.alert -%}{%- set c = c + [[wx.flag.k, '', wx.flag.glance, wx.flag.short]] -%}{%- endif -%}
{%- if wp and p is not none and p.k -%}{%- set c = c + [[p.k, p.name | upper, p.v | string, p.v | string]] -%}{%- endif -%}
{%- if wx.mm_today_k -%}{%- set c = c + [[wx.mm_today_k, ds_wtxt['rain'] | upper, MM(wx.mm_today), MM(wx.mm_today)]] -%}{%- endif -%}
{%- if wx.wind_k -%}{%- set c = c + [[wx.wind_k, ds_wtxt['wind'] | upper, WIND(), WIND()]] -%}{%- endif -%}
{%- if wx.hilo_k -%}{%- set c = c + [[wx.hilo_k, ds_wtxt['hilo'] | upper, wx.hi ~ '° / ' ~ wx.lo ~ '°', ((ds_wtxt['hilo'] | upper).split('/')[1] ~ ' ' ~ wx.lo ~ '°') if (flag_temp_low | default(true)) and (wx.lo | float(99)) <= (warning_temp_low | default(-100) | float(-100)) else ((ds_wtxt['hilo'] | upper).split('/')[0] ~ ' ' ~ wx.hi ~ '°')]] -%}{%- endif -%}
{%- set pk = ((c | selectattr(0, 'eq', 'sev') | list) + (c | selectattr(0, 'eq', 'warn') | list)) | first | default(none) -%}
{%- if wx.alert -%}{%- set pk = [wx.flag.k, '', wx.flag.glance, wx.flag.short] -%}{%- endif -%}
{{ (pk | join('§')) if pk else '' }}
{%- endmacro -%}
{#- WXDASH: pattern 'Hero dashboard', the version with forecast strips (landscape screens). Bottom up: the footer (when
     foot), the day strip (days cells, when days), the hour strip (hours cells), then the hero band between the title line
     and the hour strip's line. rows, od: the detail rows and the alert row's make-way order; op: the pollen row's (the
     last detail row while pollen is above 0); wl, wv: the detail column's widest labels and values (the pollen row's
     label is the configured type, its widest value a 3-digit count; a longer one cuts the type). On a portrait screen the detail rows form a centred block
     under a line, M above and below them, as wide as the hero group for the widest reading and never narrower than DCOLW;
     the alert row takes the first row and the pollen row the last, each in place of a row (od, op), as on the landscape screens. The hero group stacks: the number, then the icon under it a hero
     gap (hero / 7) apart by ink, centred by ink between the title line and the details' line. -#}
{#- HERO_STACK: a stacked hero group (component 'Hero group' on a portrait screen): the number centred on cx as a whole
     reading, degree sign included, and its icon a hero gap under it, counted at its nominal ink height (ICH) so the
     number keeps its height when the icon changes. cy: the number's anchor. A flagged number gets the hero chip: hugging
     the number, or from chip_x0 to chip_x1 when the layout gives them. -#}
{%- macro HERO_STACK(ns, txt, level, icon, cx, cy, hs, hic, chip_x0=none, chip_x1=none) -%}
{%- set hg = hs // EP_SPACE.heroGapDiv -%}
{%- set iu = (ICH[hic] if hic in ICH else hic) / 2 -%}
{%- set tw = HERO_INK_W(txt, hs) | int -%}
{%- set x0 = (cx - tw / 2) | round | int -%}
{%- if level -%}{{- HERO_CHIP(ns, x0 if chip_x0 is none else chip_x0, (x0 + tw - 1) if chip_x1 is none else chip_x1, cy, hs, LEVEL_FILL(level)) -}}{%- endif -%}
{{- T(ns, txt, HERO_INK_X(x0, txt, hs) | int, cy, fhero, hs, LEVEL_TEXT(level), 'lm') -}}
{%- set iy = (cy + HDN[hs] + hg + iu) | round | int -%}
{{- I(ns, icon, cx, iy, hic) -}}{{- MOON_BADGE(ns, cx, iy, hic) -}}
{%- endmacro -%}
{%- macro WXDASH(ns, title, right, stale, rows, od, wl, wv, hours, days=0, foot=false, op=[]) -%}
{%- set W, H, P, TH = EP_TK.width, EP_TK.height, EP_TK.space.pad, EP_TK.space.titleRow -%}
{%- set r = namespace(pol=none, wl=[], wv=[]) -%}{{- POLROW(r, wl, wv) -}}{%- set pol, wl, wv = r.pol, r.wl, r.wv -%}
{{- TITLE(ns, title, right, W, P, TH, stale) -}}
{%- set yb = H - P - ((FNEED(P) | int) if foot else 0) -%}
{%- set ih = EP_TK.icon.stripHour or 0 -%}
{%- if days -%}
{%- set dy = STRIPY(yb, EP_TK.icon.stripDay) | int -%}
{%- set sy = STRIPY(dy - (SPACE_S(EP_TK.type.data[1]) | int), ih) | int -%}
{%- else -%}
{%- set sy = STRIPY(yb, ih) | int -%}
{%- endif -%}
{%- if H > W -%}
{%- set dr, m = EP_TK.space.detailRow, EP_TK.space.m -%}
{%- set n = rows | length -%}
{%- set ly = sy - n * dr - 2 * m -%}
{%- set hs, hic = EP_TK.type.heroShared, EP_TK.icon.heroShared -%}{%- set hg = hs // EP_SPACE.heroGapDiv -%}
{#- the group is centred by ink (Hero group); stacked, the icon counts at its nominal ink height (ICH: the same for every
     icon of this size), so the number keeps its height when the icon changes -#}
{%- set iua = (ICH[hic] if hic in ICH else hic) / 2 -%}{%- set ida = iua -%}
{%- set cy = (P + TH + (ly - (P + TH) - (HUP[hs] + HDN[hs] + hg + iua + ida)) / 2 + HUP[hs]) | round | int -%}
{{- HERO_STACK(ns, (wx.temp | string) ~ '°', wx.temp_k, wx.icon, W // 2, cy, hs, hic) -}}
{{- L(ns, P, ly, W - P - 1, ly) -}}
{#- the detail rows: a centred block as wide as the hero group for the widest reading (-12°), never narrower than DCOLW -#}
{%- set bw = [DCOLW(wl, wv) | int, HERO_INK_W(''' + WIDEST + r''', hs) | int, ICH[hic] if hic in ICH else hic] | max -%}
{%- set bx = ((W - bw) / 2) | round | int -%}
{{- DROWS(ns, rows, wx.flag, od, bx, bx + bw - 1, (ly + sy) // 2 - (n - 1) * dr // 2, dr, EP_TK.type.fieldLabel, EP_TK.type.data, pol, op) -}}
{%- else -%}
{%- set dx = W - P - (DCOLW(wl, wv) | int) -%}
{{- HBAND(ns, ''' + HERO + r''', P + TH, sy, rows, wx.flag, od, dx, W, P, pol, op) -}}
{%- endif -%}
{{- HSTRIP(ns, sy, hours, ih, W, P) -}}
{%- if days -%}{{- DSTRIP(ns, dy, days, EP_TK.icon.stripDay, W, P) -}}{%- endif -%}
{%- if foot -%}{{- FOOT(ns, FOOT_FORECAST(), '', W, H, P, FOOT_LEVEL()) -}}{%- endif -%}
{%- endmacro -%}
{#- WXPORT: pattern 'Hero dashboard', the version with forecast strips on a portrait screen: the hero group (number, icon
     under it) with one text line under the icon, over the forecast table (hours, days, the pollen row) and the footer.
     The day rows start tomorrow (today is the hero). wind: the text line shows wind instead of today's rain. -#}
{%- macro WXPORT(ns, title, right, stale, wind) -%}
{%- set nh, nd = ''' + f'{PORT_HOURS}, {PORT_DAYS}' + r''' -%}
{%- set W, H, P, TH = EP_TK.width, EP_TK.height, EP_TK.space.pad, EP_TK.space.titleRow -%}
{{- TITLE(ns, title, right, W, P, TH, stale) -}}
{#- Bottom up, like the other weather layouts with a hero band: the footer, then the table as one block of fixed rows (3 hours, as many
     days as fit up to 3, the pollen row), each section under a line. The hero group (the number, the icon, then the line
     under them, a hero gap (hero / 7) apart by ink) is centred by ink between the title line and the table's line. The
     digits' ink is HUP / HDN around the anchor; the group itself is HERO_STACK -#}
{%- set hs, hic = EP_TK.type.heroShared, EP_TK.icon.heroShared -%}{%- set hg = hs // EP_SPACE.heroGapDiv -%}
{%- set ih = (0.417 * hic) | int -%}
{%- set ds, df = EP_TK.type.data[1], FONT[EP_TK.type.data[0]] -%}
{%- set xs, sx, rh, sl = SPACE_XS(ds) | int, SPACE_S(ds) | int, EP_TK.space.row, EP_TK.space.l -%}
{#- the line under the icon is type.data in a chip-high box (its size + 2 x space.xs) -#}
{%- set lb = ds + 2 * xs -%}
{%- set G = HUP[hs] + HDN[hs] + hg + 2 * ih + hg + lb -%}
{#- the group's ink ends at the text line's caps (a chip's fill hangs space.xs past them, as everywhere) -#}
{%- set Gi = HUP[hs] + HDN[hs] + hg + 2 * ih + hg + lb // 2 + CAPDN[ds] + 1 -%}
{%- set dd = wx.days[1:] -%}
{%- set hrs = wx.hours[1:nh + 1] if wx.hours | length > nh else wx.hours[:nh] -%}
{%- set hp = wx.pollen is not none and wx.pollen.show -%}
{#- the table ends on the footer's line, which closes its last row like the lines between the sections (a row's own
     margin already keeps its ink more than space.m from that line) -#}
{%- set yb = H - P - EP_TK.space.footer -%}
{#- fill before you float: as many day rows (up to nd) as leave the hero group a hero gap above it and space.s below it.
     The pollen row's place is always kept: without pollen one more day row takes it, so the table's top and the hero
     group stay where they are (nothing moves between states) -#}
{%- set fixed = (hrs | length) * rh + rh -%}
{%- set nd = [((yb - fixed - (P + TH) - hg - G - sx) // rh) | int, nd] | min -%}
{%- set yt = yb - fixed - nd * rh -%}
{%- set nd = nd if hp else nd + 1 -%}
{%- set cy = P + TH + (yt - (P + TH) - Gi) // 2 + HUP[hs] -%}
{#- the hero group: the number over its icon; here a flagged number's fill spans the width between the paddings -#}
{{- HERO_STACK(ns, (wx.temp | string) ~ '°', wx.temp_k, wx.icon, W // 2, cy, hs, hic, P, W - P - 1) -}}
{%- set icy = cy + HDN[hs] + hg + ih -%}
{%- set ly = icy + ih + hg + lb // 2 -%}
{#- ranges: hi°/lo° when the widest label, mm and range fit the row with space.l between them, else hi/lo everywhere (*Units and numbers*, *Ranges*) -#}
{%- set wl = namespace(l=0, m=0, r=0) -%}
{%- for d in dd[:nd] -%}{%- set wl.l = [wl.l, VALUE_W(d.d | upper, ds, df) | int] | max -%}{%- set wl.m = [wl.m, VALUE_W(MM(d.mm), ds, df) | int] | max -%}{%- set wl.r = [wl.r, VALUE_W(d.hi ~ '°/' ~ d.lo ~ '°', ds, df) | int] | max -%}{%- endfor -%}
{%- set fit = namespace(ok=(wl.l + sl + wl.m + sl + wl.r <= W - 2 * P)) -%}
{%- macro RANGE(hi, lo) -%}{{ (hi ~ '°/' ~ lo ~ '°') if fit.ok else (hi ~ '/' ~ lo) }}{%- endmacro -%}
{#- high/low · second item. The second item is the flagged item (PICK, the system-wide order) as a chip, else today's rain
     (or wind, with the wind_or_precipitation input). High/low stays unless the chip needs the whole text line -#}
{%- set pk = PICK(false) -%}
{%- set lft = RANGE(wx.hi, wx.lo) ~ ' · ' -%}
{%- set sec = (WIND()) if wind else MM(wx.mm_today) -%}
{%- set cpad = CHIP_PAD(ds) | int -%}
{%- if pk and pk.split('§')[2] == wx.hi ~ '° / ' ~ wx.lo ~ '°' -%}
{%- set kind = pk.split('§')[0] -%}
{%- set ctxt = LEVEL_MARK(kind) ~ (ds_wtxt['hilo'] | upper) ~ ' ' ~ RANGE(wx.hi, wx.lo) -%}
{%- set cwid = (VALUE_W(ctxt, ds, df) | int) + cpad -%}
{%- set rt = ' · ' ~ sec -%}
{%- set rw = VALUE_W(rt, ds, df) | int -%}
{%- if cwid + rw > W - 2 * P -%}{%- set rt, rw = '', 0 -%}{%- endif -%}
{%- set x0 = ((W - cwid - rw) / 2) | int -%}
{{- CCHIP(ns, ctxt, x0 + cwid // 2, ly, df, ds, 0, LEVEL_FILL(kind), LEVEL_TEXT(kind)) -}}
{{- T(ns, rt, x0 + cwid, ly, df, ds, color.ink, 'lm') -}}
{%- elif pk -%}
{%- set kind, lab, val, short = pk.split('§') -%}
{%- set full = LEVEL_MARK(kind) ~ ((lab ~ ' ' ~ val) if lab else val) -%}
{%- set lw = VALUE_W(lft, ds, df) | int -%}
{%- set fw = (VALUE_W(full, ds, df) | int) + cpad -%}
{%- if lw + fw <= W - 2 * P -%}{%- set ctxt = full -%}
{%- elif fw <= W - 2 * P -%}{%- set ctxt, lw, lft = full, W, '' -%}
{%- elif (VALUE_W(LEVEL_MARK(kind) ~ short, ds, df) | int) + cpad <= W - 2 * P -%}{%- set ctxt = LEVEL_MARK(kind) ~ short -%}
{%- elif wx.alert -%}{%- set ctxt = LEVEL_MARK(kind) ~ wx.flag.code -%}
{%- else -%}{%- set ctxt = FITW(LEVEL_MARK(kind) ~ short, W - 2 * P - cpad, ds, df) -%}{%- endif -%}
{%- set cwid = (VALUE_W(ctxt, ds, df) | int) + cpad -%}
{%- if lw + cwid <= W - 2 * P -%}
{%- set x0 = ((W - lw - cwid) / 2) | int -%}
{{- T(ns, lft, x0, ly, df, ds, color.ink, 'lm') -}}
{{- CCHIP(ns, ctxt, x0 + lw + cwid // 2, ly, df, ds, 0, LEVEL_FILL(kind), LEVEL_TEXT(kind)) -}}
{%- else -%}{{- CCHIP(ns, ctxt, W // 2, ly, df, ds, 0, LEVEL_FILL(kind), LEVEL_TEXT(kind)) -}}{%- endif -%}
{%- else -%}{{- T(ns, lft ~ sec, W // 2, ly, df, ds, color.ink, 'mm', W - 2 * P) -}}{%- endif -%}
{%- set y = yt -%}
{#- the forecast table: label left, mm right-aligned space.l before the temperature column (as wide as its widest value),
     temperature right; a flagged value is a row chip (row - 1 high) -#}
{%- set tc = namespace(w=0) -%}
{%- for h in hrs -%}{%- set tc.w = [tc.w, VALUE_W(h.temp ~ '°', ds, df) | int] | max -%}{%- endfor -%}
{%- for d in dd[:nd] -%}{%- set tc.w = [tc.w, VALUE_W(RANGE(d.hi, d.lo), ds, df) | int] | max -%}{%- endfor -%}
{%- set mx = W - P - 1 - tc.w - sl -%}
{%- macro RROW(ns, y, a, mm, sev, b, bk='', ak='') -%}
{#- hour labels are short ('15¦h'): the h is styled as a unit and never uppercased -#}
{%- set la = a if '¦' in a else a | upper -%}
{%- set cy = y + rh // 2 -%}
{%- if ak -%}{{- R(ns, P - sx, cy - (rh - 1) // 2, P + (VALUE_W(LEVEL_MARK(ak) ~ la, ds, df) | int) - (TAIL(ds) | int) + sx - 1, cy - (rh - 1) // 2 + rh - 2, LEVEL_FILL(ak)) -}}{%- endif -%}
{{- T(ns, LEVEL_MARK(ak) ~ la, P, cy, df, ds, LEVEL_TEXT(ak), 'lm') -}}
{%- if sev -%}{{- RCHIP(ns, LEVEL_MARK(sev) ~ MM(mm), mx, cy, df, ds, 0, 0, LEVEL_FILL(sev), LEVEL_TEXT(sev), rh) -}}
{%- else -%}{{- T(ns, MM(mm), mx, cy, df, ds, color.ink, 'rm') -}}{%- endif -%}
{%- if bk -%}{{- RCHIP(ns, LEVEL_MARK(bk) ~ b, W - P - 1, cy, df, ds, 0, 0, LEVEL_FILL(bk), LEVEL_TEXT(bk), rh) -}}
{%- else -%}{{- T(ns, b, W - P - 1, cy, df, ds, color.ink, 'rm') -}}{%- endif -%}
{%- endmacro -%}
{{- L(ns, P, y, W - P - 1, y) -}}
{%- for h in hrs -%}{{- RROW(ns, y + loop.index0 * rh, h.ts, h.mm, h.mm_k, h.temp ~ '°', h.temp_k, h.icon_k) -}}{%- endfor -%}
{%- set y = y + (hrs | length) * rh -%}
{{- L(ns, P, y, W - P - 1, y) -}}
{%- for d in dd[:nd] -%}{{- RROW(ns, y + loop.index0 * rh, d.d, d.mm, d.mm_k, RANGE(d.hi, d.lo), d.t_k, d.icon_k) -}}{%- endfor -%}
{%- if hp -%}
{#- the pollen row: type left, count right, under its line like the other sections; at warning or severe level the whole
     row is a row chip (row - 1 high), which replaces the line -#}
{%- set p = wx.pollen -%}
{%- set y = y + nd * rh -%}{%- set pcy = y + rh // 2 -%}
{%- if p.k -%}{{- R(ns, P - sx, pcy - (rh - 1) // 2, W - P - 1 + sx, pcy - (rh - 1) // 2 + rh - 2, LEVEL_FILL(p.k)) -}}
{%- else -%}{{- L(ns, P, y, W - P - 1, y) -}}{%- endif -%}
{{- T(ns, LEVEL_MARK(p.k) ~ (p.name | upper), P, pcy, df, ds, LEVEL_TEXT(p.k), 'lm', W - 2 * P - (VALUE_W(p.v, ds, df) | int) - sl) -}}
{{- T(ns, p.v, W - P - 1, pcy, df, ds, LEVEL_TEXT(p.k), 'rm') -}}
{%- endif -%}
{{- FOOT(ns, FOOT_FORECAST(), '', W, H, P, FOOT_LEVEL()) -}}
{%- endmacro -%}
'''

# Glance secondary value (one slot): the flagged item (PICK); else pollen above zero (it has priority); else hi/lo
GLANCE2 = r"""
{%- macro SECOND(ns, cx, cy, fb, s, cw, maxw=999) -%}
{%- set pk = PICK(true) -%}
{%- if pk -%}
{%- set kind, lab, val, short = pk.split('§') -%}
{%- set mark = LEVEL_MARK(kind) -%}
{%- set full = mark ~ ((lab ~ ' ' ~ val) if lab else val) -%}
{%- set pad = CHIP_PAD(s) | int -%}
{%- if (VALUE_W(full, s, fb) | int) + pad <= maxw -%}{%- set v = full -%}
{%- elif (VALUE_W(mark ~ short, s, fb) | int) + pad <= maxw -%}{%- set v = mark ~ short -%}
{%- elif wx.alert -%}{%- set v = mark ~ wx.flag.code -%}
{%- else -%}{%- set v = FITW(mark ~ short, maxw - pad, s, fb) -%}{%- endif -%}
{{- CCHIP(ns, v, cx, cy, fb, s, cw, LEVEL_FILL(kind), LEVEL_TEXT(kind)) -}}
{%- elif wx.pollen is not none and wx.pollen.show -%}
{{- T(ns, (wx.pollen.name | upper) ~ ' ' ~ wx.pollen.v, cx, cy, fb, s, color.ink, 'mm', maxw) -}}
{%- else -%}
{{- T(ns, wx.hi ~ '° / ' ~ wx.lo ~ '°', cx, cy, fb, s, color.ink, 'mm') -}}
{%- endif -%}
{%- endmacro -%}
"""

MOON_INPUT = """        moon_phase_sensor:
          name: Moon phase sensor
          description: >-
            Sensor used for the moon phase badge on the weather icon. Leave blank to detect the Moon
            integration's sensor automatically (its entity ID is translated, so it
            isn't always `sensor.moon_phase`). Set this to use a different sensor,
            such as the Lunar Phase integration's "Moon Phase" sensor. No Moon sensor means no badge.
          default: ""
          selector:
            entity:
              domain: sensor
"""
