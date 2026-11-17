"""The design system's vocabulary, applied to everything we ship and write.

rewrite(text)   the user-facing and comment wording rules (tag -> device / ESL, no 'variant', no 'Grid', ...).
                the release runs it on every blueprint it writes (lib/vocab_apply.py); it is idempotent.
lint(text)      the words that must not appear (outside URLs, code identifiers and icon names), as (line, word, text).
Both are used by lib/registry.py lint, which also checks the document and the code comments.
"""
import re

# ordered: specific before general
RULES = [
    (r'<your_tag>', '<your_device>'),
    (r"Find it under the tag's device page in", 'Find it under the device in'),
    (r'(Solum[^\n]{0,40}?)\btag\b', r'\1ESL'),
    (r'(Solum[^\n]{0,40}?)\btags\b', r'\1ESLs'),
    (r'(Developed against the \[Solum[^\]]*?)\btag\]', r'\1ESL]'),
    (r'\bWeatherman pollen variant\b', 'Weatherman pollen blueprint'),
    (r' - Pollen variant, Horizontal', ' with pollen, horizontal'),
    (r' - Pollen variant, Vertical', ' with pollen, vertical'),
    (r' - Pollen variant', ' with pollen'),
    (r'\bsingle-button variant\b', 'single-button model'),
    (r' ESLs to display', ' devices to display'),
    (r'and a summary line with the current value', 'and a footer with the current value'),
    (r'the 2.6" horizontal variant', 'the 2.6" horizontal blueprint'),
    (r'\bTags\b', 'Devices'), (r'\btags\b', 'devices'), (r'\bTag\b', 'Device'), (r'\btag\b', 'device'),
    # a drawn line is a line (a rule is a principle): tokens and the named lines
    (r'`rule\.(base|heavy|dash|tick|dot|barGap)`', r'`line.\1`'), (r'`stroke\.(series|forecastDash)`', r'`line.\1`'), (r'`rule\.\*`', '`line.*`'),
    (r'\brule\.(base|heavy|dash|tick|dot|barGap)\b', r'line.\1'), (r'\bstroke\.(series|forecastDash)\b', r'line.\1'),
    (r'\b([Tt]itle|[Ss]trip|[Bb]ase|[Hh]eavy|lower|next|vertical|[Ff]ooter|footer\'s|strip\'s|row|in-row|standard|adjacent) rule(s?)\b', r'\1 line\2'),
    (r'\b([12]) px rule\b', r'\1 px line'), (r'\b1 px-rule screens\b', '1 px-line screens'),
    (r'\brule below\b', 'line below'), (r'\b([Aa]|any|every|its|[Tt]he) rule (above|below|between|sits|itself|also|at|cutting|or)\b', r'\1 line \2'),
    (r'\btwo (fixed )?rules\b', r'two \1lines'), (r'\btheir two rules\b', 'their two lines'), (r'\bits two rules\b', 'its two lines'),
    # code comments
    (r"\(component 'Detail rows'\)", "(module 'Detail rows')"),
    (r"\(component 'Chart frame'\)", "(module 'Chart')"),
    (r"\(component 'Event list'\)", "(module 'Event list')"),
    (r"\(component 'Event hero'\)", "(module 'Event hero')"),
    (r"\(component 'Date-grouped list'\)", "(module 'Date-grouped list')"),
    (r'the Grid hero band', 'the hero band'),
    (r'as a Grid hero,', 'as a hero beside other content,'),
    (r'a 160 px Grid hero', 'a 160 px hero beside other content'),
    (r'like the other Grid weather layouts', 'like the other weather layouts with a hero band'),
    (r'\(a priority module\)', '(it has priority)'),
    (r'shared per family', 'shared per kit'), (r'5\. family kits', '5. kits'),
]
WORDS = [(r'\bGrid\b', 'Grid'), (r'\bfamil(y|ies)\b', 'family'), (r'\btags?\b', 'tag'), (r'priority module', 'priority module'),
         (r'\barchetypes?\b', 'archetype'), (r'(?<![-\w])variants?\b', 'variant'), (r'test pattern', 'test pattern'),
         (r'dash pattern', 'dash pattern'), (r'\bpresets?\b', 'preset'), (r'row kinds?', 'row kind'), (r'fallback chain', 'fallback chain'),
         (r'page frame', 'page frame'), (r'\bMatrix\b', 'Matrix'), (r'body module', 'body module'), (r'compact form', 'compact form'),
         (r'short form', 'short form'), (r'Glance hero', 'Glance hero'), (r'Grid hero', 'Grid hero'),
         (r'\b([Tt]itle|[Ss]trip|[Bb]ase|[Hh]eavy|[Ff]ooter|footer\'s) rules?\b', 'rule (a drawn line is a line)'),
         (r'\| Inputs \||\| Term \| Level \||\| Level \| CO2', 'Inputs / Level column (Arguments / Kind)'), (r'before display\b', 'display (only the HA input)'),
         (r'\bpage margins\b', 'page (only our page)'), (r'\bpattern doesn\'t recognise', 'pattern (only our pattern)')]
SKIP = re.compile(r'`[^`]*`|https?://\S+|font-family|[\w-]+-variant\b|windy-variant')


def _aliases():
    """(regex, canonical) from registry.yaml: the glossary terms' aliases and the aliases of registered names"""
    import yaml, pathlib
    r = yaml.safe_load(open(pathlib.Path(__file__).parent.parent / 'registry.yaml'))
    pairs = [(a, k) for k, als in (r.get('aliases') or {}).items() for a in als]
    pairs += [(a, k) for k, t in (r.get('terms') or {}).items() for a in (t.get('aliases') or [])]
    pairs.sort(key=lambda p: -len(p[0]))            # longest first: 'Glance secondary slot' before 'secondary slot'
    out = []
    for a, k in pairs:
        cs = any(c.isupper() for c in a)
        out.append((re.compile(r'(?<![\w`-])' + re.escape(a) + r'(?![\w`-])', 0 if cs else re.I), k))
    return out


ALIASES = _aliases()


def rewrite_aliases(text):
    """the glossary's aliases to their names (design system and code comments only: never blueprint texts, whose
    words can be on-screen titles, like the Dutch 'Agenda')"""
    def keep_case(k):
        def f(m):
            before = m.string[:m.start()]
            start = before.rstrip(' *').strip() == '' or before.rstrip(' *').endswith(('.', '|', '-', ':', '\n')) or before.endswith('\n')
            return (k[0].upper() + k[1:]) if m.group(0)[0].isupper() and start else k
        return f
    for rx, k in ALIASES:
        text = rx.sub(keep_case(k), text)
    return text


def lint_aliases(text):
    out = []
    for i, line in enumerate(text.split('\n'), 1):
        clean = SKIP.sub('', line)
        for rx, k in ALIASES:
            m = rx.search(clean)
            if m:
                out.append((i, f'{m.group(0)} → {k}', line.strip()[:110]))
    return out


def rewrite(text):
    """RULES over running text. A rule that names a code span itself (a pattern with a backtick) also applies inside
    code spans; every other rule leaves code spans alone, so `tag` in a list of banned words stays `tag`."""
    for a, b in RULES:
        if '`' in a:
            text = re.sub(a, b, text)
        else:
            text = ''.join(seg if i % 2 else re.sub(a, b, seg) for i, seg in enumerate(re.split(r'(`[^`\n]*`)', text)))
    return text


def lint_code_rules(comments):
    """in code comments a rule is a principle only as 'by rule' or 'rule N'; anything else is a drawn line"""
    out = []
    for i, line in enumerate(comments.split('\n'), 1):
        for m in re.finditer(r'\b[Rr]ules?\b', line):
            ctx = line[max(0, m.start() - 6):m.end() + 3]
            if not re.search(r'by rule|rule \d', ctx):
                out.append((i, 'rule (a drawn line is a line)', line.strip()[:110]))
    return out


def lint(text, skip_lines=()):
    out = []
    for i, line in enumerate(text.split('\n'), 1):
        if i in skip_lines or 'withdrawn' in line.lower():
            continue
        clean = SKIP.sub('', line)
        for rx, w in WORDS:
            if re.search(rx, clean, re.I if w not in ('Grid', 'Matrix', 'Glance hero', 'Grid hero') else 0):
                out.append((i, w, line.strip()[:110]))
    return out
