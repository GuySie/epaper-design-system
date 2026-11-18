"""The registry (registry.yaml): validate it, write its tables into the design system, lint the document.

  registry.py check              validate the registry (references, blueprints, screens)
  registry.py write DOC [PKG]    validate, then replace every <!-- registry:NAME --> ... <!-- /registry:NAME --> block in DOC;
                                 PKG (a blueprint package folder) is read for each page's inputs
  registry.py lint DOC [PKG]     fail on a forbidden word (lib/vocab.py) in the document, the code comments or the package,
                                 on components/modules that disagree with the registry, and on a generated block edited by hand
exit 1 on any problem.

Blocks: patterns, pages, and inputs-<page> for every live page.
"""
import sys, re, yaml, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from pixcmp_cases import B

REG = pathlib.Path(__file__).parent.parent / 'registry.yaml'
PKG = str(pathlib.Path(__file__).resolve().parent.parent / 'build')
ST = ('live', 'mock', 'reserved')


def load():
    from layouts import registry      # the registry with each page's blueprints filled in from the page definitions
    return registry()


def parse_use(u):
    m = re.fullmatch(r'([a-z-]+)(?:/([a-z-]+))?', u)
    if not m:
        raise ValueError(u)
    return m.groups()


def validate(r):
    errs = []
    scr = r['screens']
    for k, p in r['patterns'].items():
        if p['status'] not in ST:
            errs.append(f'pattern {k}: bad status')
        for v in (p.get('versions') or {}).values():
            if v['status'] not in ST:
                errs.append(f'pattern {k}: bad version status')

    for k, p in r['patterns'].items():
        for m in p.get('modules') or []:
            if m not in r['modules']:
                errs.append(f'pattern {k}: {m} is not a registered module' + (' (it is a component)' if m in r['components'] else ''))

    def use_ok(u, where):
        if u == '-':
            return
        pat, ver = parse_use(u)
        p = r['patterns'].get(pat)
        if not p:
            errs.append(f'{where}: unknown pattern {pat}')
        elif ver and ver not in (p.get('versions') or {}):
            errs.append(f'{where}: {pat} has no version {ver}')
    kinds = {}
    for n in r['components']: kinds.setdefault(n.lower(), set()).add('component')
    for n in r['modules']: kinds.setdefault(n.lower(), set()).add('module')
    for p in r['patterns'].values(): kinds.setdefault(p['name'].lower(), set()).add('pattern')
    for p in r['pages'].values(): kinds.setdefault(p['name'].lower(), set()).add('page')
    for n in (r.get('terms') or {}): kinds.setdefault(n.lower(), set()).add('term')
    # a pattern may share its name with its main module, and with a page that uses that pattern (design system: Names)
    own = {p['name'].lower() for p in r['pages'].values()
           if r['patterns'].get(parse_use(p['uses'])[0], {}).get('name', '').lower() == p['name'].lower()}
    for n, ks in kinds.items():
        if len(ks) > 1 and not ('pattern' in ks and ks <= {'pattern', 'module', 'page'} and ('page' not in ks or n in own)):
            errs.append(f'name "{n}" is used for {", ".join(sorted(ks))}')
    seen = {}
    root = pathlib.Path(__file__).parent.parent
    macros = set(re.findall(r'macro (\w+)\(', (root / 'ds_macros.jinja').read_text() + (root / 'specs' / '_wx.py').read_text()))
    for k, p in r['patterns'].items():
        for m in (p.get('macro') or '').split(', '):
            if m and m not in macros:
                errs.append(f'pattern {k}: macro {m} is not in ds_macros.jinja or specs/_wx.py')
    for k, pg in r['pages'].items():
        use_ok(pg['uses'], f'page {k}')
        for key in pg:
            if key in scr or key == 'default':
                for u in pg[key]:
                    use_ok(u, f'page {k} [{key}]')
                    if u not in ('-', pg['uses']):      # *Pages*, *One page, one pattern*
                        errs.append(f'page {k} [{key}]: {u} is not the page\'s pattern ({pg["uses"]}); the same content in '
                                    f'another pattern is a page of its own')
            elif key not in ('name', 'uses', 'status', 'blueprints', 'widest', 'drawn_also'):
                errs.append(f'page {k}: unknown key {key} (screens are {scr})')
        if pg['status'] == 'live' and not pg.get('blueprints'):
            errs.append(f'page {k}: live without a blueprint')
        for b in pg.get('blueprints') or []:
            b = str(b)
            if b not in B:
                errs.append(f'page {k}: unknown blueprint key {b}')
            if b in seen:
                errs.append(f'blueprint {b} in pages {seen[b]} and {k}')
            seen[b] = k
    for b in B:
        if b not in seen:
            errs.append(f'blueprint {b} ({B[b]}) belongs to no page')
    return errs


def name_of(r, u):
    if u == '-':
        return '—'
    pat, ver = parse_use(u)
    p = r['patterns'][pat]
    return p['name'] + (f' {p["versions"][ver]["name"]}' if ver else '')


def inputs(r, bp_key, pkg):
    class L(yaml.SafeLoader):
        pass
    L.add_multi_constructor('!', lambda l, s, n: None)
    y = yaml.load(open(f'{pkg}/{B[bp_key]}'), Loader=L)
    out = []

    def walk(d):
        for k, v in d.items():
            if isinstance(v, dict) and 'input' in v:
                walk(v['input'])
            elif k not in r['common_inputs']:
                out.append((k, (v or {}).get('name', '')))
    walk(y['blueprint']['input'])
    return out


def screen_of(fname):
    """the screen a blueprint file draws on: its layout's screen in the page definitions (lib/layouts.py)"""
    from layouts import layouts
    return next(l['screen'] for l in layouts() if l['blueprint'] == fname.split('/')[-1])


# the Vocabulary's own words (defined in the document's *Vocabulary*; the glossary points there)
VOCABULARY = ['Token', 'Component', 'Module', 'Pattern', 'Page', 'Layout', 'Blueprint', 'Version', 'Input', 'Panel', 'Device',
              'ESL', 'Tier', 'Screen', 'Canvas']


def tables(r, pkg=PKG):
    T = {}
    rows = ['| Pattern | Modules | Versions | Status | Macro |', '|---|---|---|---|---|']
    for k, p in r['patterns'].items():
        vs = '<br>'.join(f'*{v["name"]}*{"" if v["status"] == "live" else " (" + v["status"] + ")"}'
                         for v in (p.get('versions') or {}).values()) or '—'
        rows.append(f'| **{p["name"]}** | {", ".join(p["modules"])} | {vs} | {p["status"]} | ' + (', '.join(f'`{m}`' for m in p['macro'].split(', ')) if p.get('macro') else '—') + ' |')
    T['patterns'] = rows
    scr = r['screens']
    rows = ['| Page | Uses | Status | Widest reading | ' + ' | '.join(r['screen_names'][s] for s in scr) + ' |',
            '|---|---|---|---|' + '---|' * len(scr)]
    for k, pg in r['pages'].items():
        cells = []
        drawn = set(pg.get('drawn_also') or []) | {screen_of(B[str(b)]) for b in (pg.get('blueprints') or [])}
        for s in scr:
            ch = pg.get(s, pg['default'])
            n = ' or '.join(name_of(r, u) for u in ch)
            cells.append(n if n != name_of(r, pg['uses']) else ('●' if s in drawn else '○'))
        rows.append(f'| **{pg["name"]}** | {name_of(r, pg["uses"])} | {pg["status"]} | {pg.get("widest", "—")} | ' + ' | '.join(cells) + ' |')
    T['pages'] = rows
    for k, pg in r['pages'].items():
        if pg['status'] != 'live':
            continue
        # one list for the page: the inputs every one of its blueprints has, in the scheme's order, then a row per
        # screen whose blueprint differs (what it has besides, what it lacks)
        per = {str(b): [n for n, _ in inputs(r, str(b), pkg)] for b in pg['blueprints']}
        common = [n for n in next(iter(per.values()), []) if all(n in v for v in per.values())]
        code = lambda ns: ', '.join(f'`{n}`' for n in ns)
        rows = ['| Screen | Inputs of this page |', '|---|---|',
                f'| every screen | {code(common) or "—"} |']
        for b, ins in per.items():
            more, less = [n for n in ins if n not in common], [n for n in common if n not in ins]
            if more or less:
                rows.append(f'| {r["screen_names"][screen_of(B[b])]} | ' + '; '.join(
                    x for x in (('also ' + code(more)) if more else '', ('without ' + code(less)) if less else '') if x) + ' |')
        T[f'inputs-{k}'] = rows
        T[f'layouts-{k}'] = layout_rows(r, pg)
    rows = ['| Term | Kind | Part of | What it is |', '|---|---|---|---|']
    G = []
    for n, c in r['components'].items():
        G.append((n, 'component', '—', 'see *Components*'))
    # the glossary holds the words: components, modules, the registry's terms and the Vocabulary's own words. Pattern,
    # version and page names are not in it: the Patterns and Pages tables are their index
    for n in r['modules']:
        G.append((n, 'module', '—', 'see *Modules*'))
    for n in VOCABULARY:
        G.append((n, 'vocabulary', '—', 'see *Vocabulary*'))
    for n, t in (r.get('terms') or {}).items():
        G.append((n, t['level'], t.get('of') or '—', t['what']))
    al = {}
    for k, als in (r.get('aliases') or {}).items():
        al.setdefault(k.lower(), []).extend(als)
    for n, t in (r.get('terms') or {}).items():
        al.setdefault(n.lower(), []).extend(t.get('aliases') or [])
    for n, lv, of, what in sorted(G, key=lambda g: g[0].lower()):
        other = al.get(n.lower())
        rows.append(f'| **{n}** | {lv} | {of} | {what}' + (f' (not: {", ".join(other)})' if other else '') + ' |')
    T['glossary'] = rows
    out = {k: '\n'.join(v) for k, v in T.items()}
    from tier_tables import tables as tier_tables
    out.update(tier_tables())        # tier-type, tier-space, tier-icon: generated from ep_tokens.jinja
    return out


def layout_rows(r, pg):
    """a page's layouts, one row each: the measured sizes (ep_tokens.jinja EP_LAYOUT), the forecast cells its spec names
    (HOURS, DAYS), and the kinds of state its check cases cover (lib/coverage.py), with how many cases it has"""
    from tier_tables import load_layouts
    from coverage import COVERAGE
    from pixcmp_cases import CASES, EXTRA_CASES
    from build_lib import load_spec
    from layouts import layouts
    L = {l['key']: l for l in layouts()}
    tok = load_layouts()
    keys = [str(b) for b in pg['blueprints']]
    hero = any((tok[k]['type'].get('heroAlone') or tok[k]['type'].get('heroShared')) for k in keys)
    cells = any(getattr(load_spec(L[k]['spec']), 'HOURS', None) is not None for k in keys)
    head = ['Screen'] + (['Hero', 'Hero icon'] if hero else []) + (['Hour / day cells'] if cells else []) + ['Checked in', 'Not applicable', 'Cases']
    rows = ['| ' + ' | '.join(head) + ' |', '|' + '---|' * len(head)]
    for k in keys:
        t, sp, cov = tok[k], load_spec(L[k]['spec']), COVERAGE[k]
        row = [r['screen_names'][L[k]['screen']]]
        if hero:
            h = t['type'].get('heroAlone') or t['type'].get('heroShared')
            st = t['icon'].get('heroAloneSteps')
            row += [f'{h} px' if h else '—', (f'{st[0]} → {st[-1]} px' if st else (f"{t['icon']['heroShared']} px" if t['icon'].get('heroShared') else '—'))]
        if cells:
            row.append(f'{sp.HOURS} / {sp.DAYS or "—"}' if getattr(sp, 'HOURS', None) is not None else '—')
        row.append(', '.join(kind for kind, v in cov.items() if not v.startswith('n/a:') and v != 'GAP'))
        row.append(', '.join(kind for kind, v in cov.items() if v.startswith('n/a:')) or '—')
        row.append(str(len({c[0] for c in list(CASES) + list(EXTRA_CASES) if c[1] == k})))
        rows.append('| ' + ' | '.join(row) + ' |')
    return rows


INLINE = re.compile(r'(<!-- v:([A-Za-z0-9_.:-]+) -->)(.*?)(<!-- /v -->)')   # a value inside typed text (lib/doc_values.py)
BLOCK = re.compile(r'(<!-- registry:([a-z0-9-]+) -->\n)(.*?)(<!-- /registry:\2 -->)', re.S)


README = pathlib.Path(__file__).resolve().parent.parent.parent / 'README.md'
README_TABLES = {'blueprints', 'pictures'}


def blueprint_rows(pkg=PKG):
    """the README's blueprint table: each built blueprint's name and the first paragraph of its description (what it shows)"""
    rows = ['| Blueprint | Page | Shows |', '|---|---|---|']
    for f in sorted(pathlib.Path(pkg).glob('epaper-blueprint-*.yaml')):
        bp = yaml.load(f.read_text(encoding='utf-8'), Loader=_Tagless)['blueprint']
        paras = [x.strip() for x in bp['description'].split('\n\n') if x.strip() and not x.strip().startswith('#')]
        name = re.sub(r'^E-paper ', '', bp['name'])
        rows.append(f'| [`{f.name}`](blueprints/{f.name}) | {name} | {" ".join(paras[0].split())} |')
    return rows


def picture_rows(pkg=PKG):
    """the README's pictures: per page its blueprints, each with its name and its reference picture (lib/pictures.py)"""
    import pictures
    out, page = [], None
    for pname, f, _, _ in pictures.picks():
        if pname != page:
            out += ['', f'**{pname}**', '']
            page = pname
        bp = yaml.load((pathlib.Path(pkg) / f).read_text(encoding='utf-8'), Loader=_Tagless)['blueprint']
        name = re.sub(r'^E-paper ', '', bp['name'])
        out += [f'{name}', '', f'![{name}](docs/images/{pathlib.Path(f).stem}.png)', '']
    return out[1:-1]


class _Tagless(yaml.SafeLoader):
    """reads a blueprint's !input tags as plain values"""


_Tagless.add_multi_constructor('!', lambda loader, tag, node: None)


def write(doc, pkg=PKG):
    r = load(); T = tables(r, pkg)
    T['blueprints'] = '\n'.join(blueprint_rows(pkg))
    T['pictures'] = '\n'.join(picture_rows(pkg))
    own = README_TABLES if pathlib.Path(doc).resolve() == README else set(T) - README_TABLES
    T = {k: v for k, v in T.items() if k in own}
    s = open(doc).read()
    names, unknown = set(), set()

    def rep(m):
        n = m.group(2)
        if n not in T:
            unknown.add(n); return m.group(0)
        names.add(n)
        return m.group(1) + T[n] + '\n' + m.group(4)
    s2 = BLOCK.sub(rep, s)
    import doc_values

    def val(m):
        try:
            return m.group(1) + doc_values.value(m.group(2)) + m.group(4)
        except (KeyError, AttributeError, ValueError):
            unknown.add('v:' + m.group(2)); return m.group(0)
    s2 = INLINE.sub(val, s2)
    open(doc, 'w').write(s2)
    return set(T) - names, unknown


def table_names(text, heading):
    """the bold names in the first column of the first table under '## heading'"""
    i = text.index(f'\n## {heading}\n'); j = min(k for k in (text.find('\n## ', i + 5), text.find('\n### ', i + 5), len(text)) if k > 0)
    return {m.group(1): m.group(2) for m in re.finditer(r'^\| \*\*(.+?)\*\* \| ([a-z]+ \|)?', text[i:j], re.M)}


def lint_parts(r, doc_text):
    """components and modules: document tables and code comments agree with the registry"""
    errs = []
    comp = table_names(doc_text, 'Components'); mods = table_names(doc_text, 'Modules')
    for n, lv in comp.items():
        if n not in r['components']:
            errs.append(f'Components table: {n} is not a registry component')
    for n in r['components']:
        if n not in comp:
            errs.append(f'Components table: {n} missing')
    for n in mods:
        if n not in r['modules']:
            errs.append(f'Modules table: {n} is not a registry module')
    for n in r['modules']:
        if n not in mods:
            errs.append(f'Modules table: {n} missing')
    root = pathlib.Path(__file__).parent.parent
    for f in ['ds_macros.jinja', 'lib/ep_tokens.jinja'] + sorted(str(p.relative_to(root)) for p in (root / 'specs').glob('*.py')):
        t = (root / f).read_text()
        for kind, n in re.findall(r"\((component|module) '([^']+)'\)", t):
            if kind == 'component' and n not in r['components']:
                errs.append(f"{f}: (component '{n}') is {'a module' if n in r['modules'] else 'unknown'}")
            if kind == 'module' and n not in r['modules']:
                errs.append(f"{f}: (module '{n}') is {'a component' if n in r['components'] else 'unknown'}")
    return errs


def lint_words(doc_text, pkg):
    """the vocabulary's forbidden words: document, code comments, the package"""
    from vocab import lint as vlint
    from vocab_apply import CODE, JCOM
    errs = []
    root = pathlib.Path(__file__).parent.parent
    body = BLOCK.sub(lambda m: m.group(1) + m.group(4), doc_text)
    for i, w, line in vlint(body):
        errs.append(f'document line {i}: "{w}": {line}')
    # Atomic Design's level names appear only in the Vocabulary's mapping (its table and the sentence naming it)
    mapping = re.compile(r'^\| \*\*(Token|Component|Module|Pattern|Page|Layout|Blueprint)\*\* \||Atomic Design')
    for i, line in enumerate(body.split('\n'), 1):
        if mapping.search(line):
            continue
        for m in re.finditer(r'(?i)\b(atoms?|molecules?|organisms?)\b', re.sub(r'`[^`]*`', '', line)):
            errs.append(f'document line {i}: Atomic Design word "{m.group(0)}" (use our terms): {line.strip()[:90]}')
    from vocab import lint_aliases
    body2 = re.sub(r'`[^`\n]*`', '', body)
    for i, w, line in lint_aliases(body2):
        if '(not: ' in line:
            continue
        errs.append(f'document line {i}: alias {w}: {line}')
    for f in CODE:
        t = (root / f).read_text()
        com = '\n'.join(JCOM.findall(t)) + '\n' + '\n'.join(l for l in t.split('\n') if re.match(r'^\s*#', l))
        for i, w, line in vlint(com):
            errs.append(f'{f} comment: "{w}": {line}')
        for i, w, line in lint_aliases(com):
            errs.append(f'{f} comment: alias {w}: {line}')
        for i, l in enumerate(com.split('\n'), 1):
            for m in re.finditer(r'(?i)\b(atoms?|molecules?|organisms?)\b', l):
                errs.append(f'{f} comment: Atomic Design word "{m.group(0)}": {l.strip()[:90]}')
        for i, l in enumerate(com.split('\n'), 1):
            for rx, why in [(r'\bdisplay\b(?!s)(?![_-])', 'display (only the HA input displays)'), (r'spec module', 'module (a Python file is a file)'),
                            (r'top-level', 'level (severity only)'), (r'\bpanel input\b', 'panel height input')]:
                if re.search(rx, re.sub(r'`[^`]*`', '', l)):
                    errs.append(f'{f} comment: {why}: {l.strip()[:90]}')
        from vocab import lint_code_rules
        for i, w, line in lint_code_rules(com):
            errs.append(f'{f} comment: {w}: {line}')
    if pkg:
        import glob
        for f in sorted(glob.glob(f'{pkg}/*.yaml')) + glob.glob(f'{pkg}/README.md') + sorted(glob.glob(f'{pkg}/custom_templates/*.jinja')):
            t = open(f).read()
            if f.endswith('.jinja'):
                t = '\n'.join(JCOM.findall(t))
            for i, w, line in vlint(t):
                errs.append(f'{pathlib.Path(f).name}: "{w}": {line}')
    return errs


# ordinary uses of a multi-word page or pattern name (not the name): exact text around it
CAPS_OK = ['a dry rain forecast', 'a bar or line chart', 'the 24 h line chart', 'An appliance run', 'The hero is a word (bin day, room sign',
           'with a phone: guest Wi-Fi', 'sun & moon track)', "today's path is a line chart"]

REF_OK = ['Fixed rows', 'The generator', 'Same pixels, same spec', 'A label never overlaps its value', 'Mark data as stale after', 'Rain or wind',
          'Header title', 'Hour cell / Day cell']


def lint_names(r, doc_text):
    """page and pattern names are proper names: a multi-word name in lowercase is a slip, unless it is also a module name
    or an ordinary use listed in CAPS_OK. Every glossary term appears in the document outside the glossary."""
    errs = []
    body = re.sub(r'`[^`\n]*`', '', BLOCK.sub(lambda m: m.group(1) + m.group(4), doc_text))
    mods = {m.lower() for m in r['modules']}
    names = [p['name'] for p in r['patterns'].values()] + [p['name'] for p in r['pages'].values()]
    for n in names:
        n = re.sub(r' \(.*\)$', '', n)
        if ' ' not in n or n.lower() in mods:
            continue
        lo = n[0].lower() + n[1:]
        for m in re.finditer(r'(?<![\w-])' + re.escape(lo) + r'(?![\w-])', body):
            ctx = body[max(0, m.start() - 45):m.end() + 45]
            if any(ok in ctx for ok in CAPS_OK) or re.match(r'\| \d', body[body.rfind('\n', 0, m.start()) + 1:m.start() + 3]):
                continue
            errs.append(f'document: page/pattern name in lowercase "{lo}" (write "{n}"): …{ctx.strip()}…'.replace('\n', ' '))
    # a cross-reference (an italic name after see / in / under / with / follows, or in brackets) names a heading or a
    # named part; REF_OK lists the bold rules and inputs that are referred to by name
    heads = {re.sub(r'^#+ ', '', l).strip() for l in doc_text.split('\n') if l.startswith('#')}
    parts = set(r['components']) | set(r['modules']) | {p['name'] for p in r['patterns'].values()} | \
        {pg['name'] for pg in r['pages'].values()} | set(r.get('terms') or {})
    for m in re.finditer(r'(?:\bsee|\bin|\bunder|\bwith|\bfollows|\() ?\*([A-Z][^*\n]{2,40})\*', body):
        n = m.group(1)
        if n not in heads and n not in parts and n not in REF_OK:
            errs.append(f'document: reference *{n}* is not a heading or a named part')
    # a rule is referred to by its name, never its number (*Section*, *Rule name*): the name is the start of a bold lead
    # of a list item in that section, so a rule that is added, removed or renamed can't leave a reference pointing elsewhere
    for m in re.finditer(r'\*[^*\n]+\*,? rules? \d+', doc_text):
        errs.append(f'document: "{m.group(0)}" refers to a rule by number (write *Section*, *Rule name*)')
    leads, sec = {}, None
    versions = {f'{p["name"]} {v["name"]}' for p in r['patterns'].values() for v in (p.get('versions') or {}).values()}
    for l in doc_text.split('\n'):
        if l.startswith('#'):
            sec = re.sub(r'^#+ ', '', l).strip()
        for b in re.findall(r'^\s*(?:-|\d+\.)\s+\*\*([^*]+)\*\*', l):
            leads.setdefault(sec, []).append(b.rstrip('.:').lower())
    for m in re.finditer(r'\*([^*\n]+)\*, \*([^*\n]+)\*((?: and \*[^*\n]+\*)*)', doc_text):
        sec = m.group(1)
        for n in [m.group(2)] + re.findall(r'\*([^*\n]+)\*', m.group(3)):
            if sec not in heads or n in heads or n in parts or n in REF_OK or n in versions:
                continue
            if not any(b == n.lower() or b.startswith(n.lower() + ' ') or b.startswith(n.lower() + ',') or b.startswith(n.lower() + ':')
                       for b in leads.get(sec, [])):
                errs.append(f'document: *{sec}*, *{n}* names no rule in that section')
    # a word written twice in a row ("the glance Glance secondary") is a slip of the alias rewrite
    for m in re.finditer(r'(?i)\b([a-z]{3,})[ \t]+\1\b', body):
        errs.append(f'document: "{m.group(0)}" repeats a word')
    for m in re.finditer(r'\*\*([^*]{3,40})\*\* is the \1\b', body):
        errs.append(f'document: "{m.group(0)}" says a name is itself')
    gi = doc_text.find('<!-- registry:glossary -->'); gj = doc_text.find('<!-- /registry:glossary -->', gi)
    rest = (doc_text[:gi] + doc_text[gj:]) if gi >= 0 else doc_text
    for t in r.get('terms', {}):
        name = re.sub(r' \(.*\)$', '', t if isinstance(t, str) else t.get('name', ''))
        if name and not re.search(r'(?i)(?<![\w-])' + re.escape(name) + r'(?![\w-])', rest):
            errs.append(f'glossary term "{name}" is not used in the document')
    return errs


def lint(doc, pkg=PKG):
    r = load(); T = tables(r, pkg); errs = []
    s = open(doc).read()
    errs += lint_parts(r, s)
    errs += lint_names(r, s)
    errs += lint_words(s, pkg)
    for m in BLOCK.finditer(s):
        if m.group(2) in T and m.group(3) != T[m.group(2)] + '\n':
            errs.append(f'generated block {m.group(2)} edited by hand: run registry.py write')
    import doc_values
    seen = {}                               # *Thresholds*: the same data has the same inputs, names and defaults everywhere
    import pages
    for page in pages.names():
        for i in pages.load(page).get('inputs') or []:
            if i['name'].startswith(('warning_', 'severe_')):
                if i['name'] in seen and seen[i['name']][1] != i.get('default'):
                    errs.append(f"threshold {i['name']}: default {i.get('default')!r} on {page}, {seen[i['name']][1]!r} on {seen[i['name']][0]}")
                seen.setdefault(i['name'], (page, i.get('default')))
    for m in INLINE.finditer(s):
        try:
            if m.group(3) != doc_values.value(m.group(2)):
                errs.append(f'value v:{m.group(2)} edited by hand ({m.group(3)!r}): run registry.py write')
        except (KeyError, AttributeError, ValueError):
            errs.append(f'value v:{m.group(2)}: no such value (lib/doc_values.py)')
    return errs


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else ''
    if cmd not in ('check', 'write', 'lint') or (cmd != 'check' and len(sys.argv) < 3):
        sys.exit(__doc__)
    pkg = sys.argv[3] if len(sys.argv) > 3 else PKG
    r = load(); errs = validate(r)
    if cmd == 'write' and not errs:
        miss, unknown = write(sys.argv[2], pkg)
        if pathlib.Path(sys.argv[2]).resolve() != README:      # the README's blueprint table is written with the design system
            m2, u2 = write(str(README), pkg)
            miss |= m2; unknown |= u2
        if miss:
            errs.append(f'no block in the doc for: {", ".join(sorted(miss))}')
        if unknown:
            errs.append(f'blocks the registry doesn\'t make: {", ".join(sorted(unknown))}')
    if cmd == 'lint':
        errs += lint(sys.argv[2], pkg)
    for e in errs:
        print('ERROR', e)
    print(f'registry: {len(r["patterns"])} patterns, {len(r["pages"])} pages, {len(errs)} problems')
    sys.exit(1 if errs else 0)
