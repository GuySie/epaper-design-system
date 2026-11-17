#!/usr/bin/env python3
"""One input scheme for every blueprint (design system: Blueprint mechanics, Input sections).

  inputs_std.py PKG        rewrite every blueprint in PKG to the scheme (idempotent)
  inputs_std.py --lint PKG report every blueprint that breaks the scheme; exit 1 when one does

The scheme: five sections, always in this order, each only when it has inputs.
  display     Display and schedule (open):  displays, button_entity, automation_trigger, automation_conditions
  content     Content (open):               the page's main entity first (required), then its other entities, then options
  thresholds  Thresholds (collapsed):       flag_<what>, warning_<what>, severe_<what> for each reading
  appearance  Appearance (collapsed):       header_title, location_string, time_format, weekday_format, rotate
  advanced    Advanced (collapsed):         stale_after, led_color, led_flash_delay, font_dir
Required: displays, the main entity (MAIN), and the trigger. Everything else has a default.
Only the input names change; the blueprint's variables keep the names the drawing reads.
"""
import glob, os, re, sys

SECTIONS = [
    ('display', 'Display and schedule', 'mdi:monitor', False,
     ['displays', 'button_entity', 'automation_trigger', 'automation_conditions']),
    ('content', 'Content', 'mdi:view-list', False, None),
    ('thresholds', 'Thresholds', 'mdi:alert-outline', True, None),
    ('appearance', 'Appearance', 'mdi:palette-outline', True,
     ['header_title', 'location_string', 'time_format', 'weekday_format', 'rotate']),
    ('advanced', 'Advanced', 'mdi:cog', True, ['stale_after', 'led_color', 'led_flash_delay', 'font_dir']),
]
SCALE = []   # the page sets its chart scale; never an input (design system: Chart frame, item 2)

# the page's main entity: required, first in Content
MAIN = {'weather': 'weather_entity', 'appointment': 'calendar_entities', 'calendar': 'calendar_entities',
        'entities': 'entity_1', 'plant-moisture': 'plant_1', 'claude-usage': 'bar_1', 'doors-windows': 'openings',
        'co2-graph': 'co2_entity', 'medication': 'button_entity', 'rain-forecast': None, 'sun-moon': None}
OPTIONAL_DEFAULT = {'location_string': '""'}


def part(fname, table):
    for k, v in table.items():
        if k in fname:
            return v
    return None


def block_end(lines, i, indent):
    j = i + 1
    while j < len(lines) and (not lines[j].strip() or len(lines[j]) - len(lines[j].lstrip()) > indent):
        j += 1
    return j


SEC = {}


def parse(lines):
    """input block -> (start, end, [(name, lines relative to indent 0)]) in file order"""
    s = lines.index('  input:')
    e = block_end(lines, s, 2)
    items, i = [], s + 1
    while i < e:
        if not lines[i].strip():
            i += 1
            continue
        j = block_end(lines, i, 4)
        blk = lines[i:j]
        name = blk[0].strip().rstrip(':')
        if '      input:' in blk:
            k = blk.index('      input:')
            sub = blk[k + 1:]
            m = 0
            while m < len(sub):
                if not sub[m].strip():
                    m += 1
                    continue
                n = block_end(sub, m, 8)
                items.append((sub[m].strip().rstrip(':'), [l[8:] for l in sub[m:n]]))
                SEC[items[-1][0]] = name
                m = n
        else:
            items.append((name, [l[4:] for l in blk]))
            SEC[name] = None
        i = j
    while e > s and not lines[e - 1].strip():
        e -= 1
    return s, e, items


def drop_default(blk):
    out, skip = [], False
    for l in blk:
        if re.match(r'^  default:', l):
            skip = True
            continue
        if skip and (l.startswith('   ') or not l.strip()):
            continue
        skip = False
        out.append(l)
    return out


def section_of(name):
    for key, _, _, _, names in SECTIONS:
        if names and name in names:
            return key
    if re.match(r'^(flag|warning|severe)_', name) or name in SCALE:
        return 'thresholds'
    return 'content'


def threshold_order(names):
    whats = []
    for n in names:
        if n in SCALE:
            continue
        w = re.sub(r'^(flag|warning|severe)_', '', n)
        if w not in whats:
            whats.append(w)
    out = []
    for w in whats:
        out += [p + w for p in ('flag_', 'warning_', 'severe_') if p + w in names]
    return out + [n for n in SCALE if n in names]


def is_entity(blk):
    return any(re.match(r'^      entity:', l) or re.match(r'^    entity:', l) for l in blk)


def standardise(path):
    fname = os.path.basename(path)
    text = open(path, encoding='utf-8').read()
    lines = text.split('\n')
    s, e, items = parse(lines)
    main = part(fname, MAIN)
    blocks = {}
    for nn, blk in items:
        if nn == main or nn == 'displays':
            blk = drop_default(blk)
        if nn in OPTIONAL_DEFAULT and not any(re.match(r'^  default:', l) for l in blk):
            blk = blk[:2] + [f'  default: {OPTIONAL_DEFAULT[nn]}'] + blk[2:]
        blocks[nn] = blk
    order = {k: [] for k, *_ in SECTIONS}
    for n in blocks:
        order[section_of(n)].append(n)
    for key, _, _, _, names in SECTIONS:
        if names:
            order[key] = [n for n in names if n in order[key]]
    order['thresholds'] = threshold_order(order['thresholds'])
    c = order['content']
    first = [main] if main in c else []
    order['content'] = first + [n for n in c if n not in first and is_entity(blocks[n])] + \
                       [n for n in c if n not in first and not is_entity(blocks[n])]
    out = ['  input:']
    for key, title, icon, collapsed, _ in SECTIONS:
        if not order[key]:
            continue
        out += [f'    {key}:', f'      name: {title}', f'      icon: "{icon}"'] + \
               (['      collapsed: true'] if collapsed else []) + ['      input:']
        for n in order[key]:
            out += ['        ' + l if l.strip() else '' for l in blocks[n]]
    lines = lines[:s] + out + lines[e:]
    text = '\n'.join(lines)
    open(path, 'w', encoding='utf-8').write(text)


# words a label may capitalise after its first word: proper names and words that follow a colon
PROPER = {'Claude', 'Moon', 'Kleenex', 'Home', 'Assistant', 'OpenDisplay', 'Wi-Fi', 'Sun', 'Meteoalarm'}


def lint(path):
    """problems with one blueprint against the scheme"""
    fname = os.path.basename(path)
    lines = open(path, encoding='utf-8').read().split('\n')
    SEC.clear()
    s, e, items = parse(lines)
    errs = []
    top = [l.strip().rstrip(':') for l in lines[s + 1:e] if re.match(r'^    \w+:$', l)]
    keys = [k for k, *_ in SECTIONS]
    if [t for t in top if t not in keys]:
        errs.append(f'inputs outside a section: {[t for t in top if t not in keys]}')
    if top != [k for k in keys if k in top]:
        errs.append(f'sections out of order: {top}')
    names = [n for n, _ in items]
    for n, blk in items:
        if SEC.get(n) and SEC[n] != section_of(n):
            errs.append(f'{n} is in {SEC[n]}, belongs in {section_of(n)}')
    th = [n for n in names if section_of(n) == 'thresholds']
    if th != threshold_order(th):
        errs.append(f'thresholds out of order: {th}')
    main = part(fname, MAIN)
    for n, blk in items:
        has_def = any(re.match(r'^  default:', l) for l in blk)
        if n in ('displays', 'automation_trigger', main):
            if has_def and n != 'automation_trigger':
                errs.append(f'{n} is required but has a default')
        elif not has_def:
            errs.append(f'{n} is optional but has no default')
        if 'threshold' in n or n in ('warning_after', 'severe_after'):
            errs.append(f'{n}: thresholds are named warning_<what> / severe_<what>')
    for n, blk in items:                       # labels are in sentence case: only the first word and proper names are capitalised
        for l in blk:
            m = re.match(r"^  name: (.+)$", l)
            if m:
                words = m.group(1).strip("'\"").split()
                caps = [w for w in words[1:] if w[:1].isupper() and w.strip('():,.') not in PROPER and not w.strip('():,.').isupper()]
                if caps:
                    errs.append(f'{n}: label {m.group(1)!r} is not in sentence case ({", ".join(caps)})')
    for o in ('display',):
        if o in names:
            errs.append('`display`: the device input is always `displays`')
    for n in ('y_min', 'y_max', 'graph_cap_mm_h'):
        if n in names:
            errs.append(f'{n}: the page sets its chart scale, so it is never an input')
    if 'panel_height' in names:
        errs.append('panel_height: one blueprint per screen, so the panel is never an input')
    return errs


if __name__ == '__main__':
    if sys.argv[1] == '--lint':
        bad = 0
        for f in sorted(glob.glob(f'{sys.argv[2]}/epaper-*.yaml')):
            for m in lint(f):
                bad += 1
                print(f'{os.path.basename(f)}: {m}')
        print(f'{bad} problems')
        sys.exit(1 if bad else 0)
    for f in sorted(glob.glob(f'{sys.argv[1]}/epaper-*.yaml')):
        standardise(f)
        print('ok', os.path.basename(f))
