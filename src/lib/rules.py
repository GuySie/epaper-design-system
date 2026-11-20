#!/usr/bin/env python3
"""The words are the source: which code follows which rule of the design system, and whether it still does.

Code that decides what is drawn cites the rule it implements, in a comment or a check's message, as the document refers
to a rule itself: `*Section*`, or `*Section*, Rule name` (the rule's name is the bold lead of a list item, or the first
cell of a table row, in that section).

  rules.py lint DOC     every citation names a section, and a rule in it, that the document has (a rule that is renamed or
                        removed stops the build until the code follows); and no cited rule's text has changed since the
                        code that cites it was last confirmed (lib/rules.lock.json)
  rules.py accept DOC   confirm: the code that cites the changed rules has been read against their new text
  rules.py trace DOC    the trace table: each cited rule and where it is implemented or checked; then the rules of the
                        document that nothing cites

A changed rule is found by a fingerprint of its text (generated values and tables left out, so a regenerated number is
not a changed rule).
"""
import hashlib, json, pathlib, re, sys
LIB = pathlib.Path(__file__).resolve().parent
SRC = LIB.parent
LOCK = LIB / 'rules.lock.json'
CODE = ['ds_macros.jinja', 'check.py', 'lib/layout_fit.py', 'lib/derive_tokens.py', 'lib/hero_metrics.py', 'lib/build_lib.py',
        'wx_steps.yaml'] + sorted(f'specs/{f.name}' for f in (SRC / 'specs').glob('*.py'))
CITE = re.compile(r'\*([A-Z][^*\n]{1,60})\*(?:, \*?([A-Za-z`][^*\n.;:)\]]{2,60}?)\*?(?=[.;:)\]\n]|$| and | or |, \*))?')
BLOCK = re.compile(r'<!-- registry:([a-z0-9-]+) -->\n.*?<!-- /registry:\1 -->', re.S)
INLINE = re.compile(r'<!-- v:[^>]*-->.*?<!-- /v -->')


def norm(s):
    return re.sub(r'\s+', ' ', re.sub(r'[`*]', '', s)).strip().lower().rstrip('.:,')


def document(path):
    """{section: {'': its own text, rule name: that rule's text}}; a rule is a list item with a bold lead, or a table row"""
    text = INLINE.sub('', BLOCK.sub('', pathlib.Path(path).read_text()))
    out, sec, cur = {}, None, None
    for line in text.split('\n'):
        h = re.match(r'#+ (.+)', line)
        if h:
            sec, cur = h.group(1).strip(), None
            out[sec] = {'': ''}
            continue
        if sec is None:
            continue
        lead = re.match(r'\s*(?:-|\d+\.)\s+\*\*([^*]+)\*\*', line)
        row = re.match(r'\| ?(?:\*\*)?([^|*]+?)(?:\*\*)? ?\|', line) if line.startswith('|') and not line.startswith('|-') else None
        if lead:
            cur = norm(lead.group(1))
            out[sec][cur] = ''
        elif row:
            out[sec].setdefault(norm(row.group(1)), '')
            out[sec][norm(row.group(1))] += line + '\n'
            cur = None
        elif not line.strip() or not line.startswith((' ', '\t')) and not re.match(r'\s*(?:-|\d+\.)\s', line):
            cur = None
        out[sec]['' if cur is None else cur] += line + '\n' if not row else ''
    return out


def find(doc, sec, rule):
    """the rule's key in its section: the name, or a name that starts with it"""
    r = norm(rule)
    keys = [k for k in doc[sec] if k]
    return next((k for k in keys if k == r), None) or next((k for k in keys if k.startswith(r + ' ') or k.startswith(r + ',') or k.startswith(r + ':')), None)


def citations():
    """[(file, line number, section, rule or None)] from the comments and messages of the code that draws and checks"""
    out = []
    for rel in CODE:
        for n, line in enumerate((SRC / rel).read_text().split('\n'), 1):
            if rel.endswith('.jinja') and '{#' not in line and '#}' not in line and not line.lstrip().startswith(('the ', 'a ', '(', '*')) and '*' not in line[:3] and '-#}' not in line:
                if '{{' in line or '{%' in line:
                    continue
            for m in CITE.finditer(line):
                out.append((rel, n, m.group(1).strip(), (m.group(2) or '').strip() or None))
    return out


def resolve(doc):
    """(good, problems): good = {(section, rule key or ''): [(file, line)]}"""
    good, bad = {}, []
    for rel, n, sec, rule in citations():
        if sec not in doc:
            if re.fullmatch(r'[A-Z][a-z]+( [a-z&]+)*', sec) and len(sec.split()) <= 6:
                bad.append(f'{rel}:{n}: *{sec}* is no section of the design system')
            continue
        key = ''
        if rule:
            key = find(doc, sec, rule)
            if key is None:
                # words after a section that name no rule are a remark, unless they are written as a rule name (italic)
                key = ''
        good.setdefault((sec, key), []).append((rel, n))
    return good, bad


def prints(doc, good):
    return {f'{s} / {k}' if k else s: hashlib.sha1(norm(doc[s][k]).encode()).hexdigest()[:12] for (s, k) in good}


def main():
    cmd, path = (sys.argv[1:] + ['', ''])[:2]
    if cmd not in ('lint', 'accept', 'trace') or not path:
        sys.exit(__doc__)
    doc = document(path)
    good, bad = resolve(doc)
    now = prints(doc, good)
    if cmd == 'accept':
        LOCK.write_text(json.dumps(now, indent=1, sort_keys=True, ensure_ascii=False) + '\n')
        print(f'rules: {len(now)} cited rules confirmed')
        return
    if cmd == 'trace':
        for (s, k), where in sorted(good.items()):
            files = sorted({f for f, _ in where})
            print(f"*{s}*{', ' + k if k else ''}: " + ', '.join(f"{f} ({sum(1 for g, _ in where if g == f)})" for f in files))
        cited = {(s, k) for s, k in good}
        cited_secs = {s for s, _ in good}
        loose = [(s, k) for s in doc for k in doc[s] if k and (s, k) not in cited and not k.startswith('`')]
        print(f'\n{len(good)} rules cited by code, in {len(cited_secs)} sections; {len(loose)} named rules that nothing cites by name '
              f'({sum(1 for s, _ in loose if s not in cited_secs)} of them in sections no code cites at all)')
        return
    old = json.loads(LOCK.read_text()) if LOCK.exists() else {}
    for k, h in sorted(now.items()):
        if k in old and old[k] != h:
            s, _, r = k.partition(' / ')
            where = good[(s, r)]
            bad.append(f"the rule *{s}*{', ' + r if r else ''} has changed: read the code that cites it against its new text ("
                       + ', '.join(sorted({f'{f}:{n}' for f, n in where})[:6]) + (' …' if len(where) > 6 else '') + '), then run rules.py accept')
    new = [k for k in now if k not in old]
    for e in bad:
        print('ERROR', e)
    print(f'rules: {len(now)} cited rules, {len(new)} not yet confirmed, {len(bad)} problems')
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
