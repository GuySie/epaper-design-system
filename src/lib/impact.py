#!/usr/bin/env python3
"""Which pages a change to the kit can reach (CLAUDE.md, How a change goes, steps 2 and 8).

  impact.py MACRO [MACRO ...]   the layouts that draw with these macros, directly or through other macros, by page
  impact.py --diff [REF]        the same for every macro whose text differs from git REF (default HEAD), in
                                ds_macros.jinja and in the shared spec pieces (specs/_*.py)

A layout draws with a macro when its spec calls it, or calls a macro that calls it. The list says which pages' sections
to read again before a change, and which pages a result has to name; it doesn't say that their pixels change (the
reference comparison does that).
"""
import importlib.util, pathlib, re, subprocess, sys
LIB = pathlib.Path(__file__).resolve().parent
SRC = LIB.parent
sys.path[:0] = [str(LIB), str(SRC / 'specs')]

OPEN = re.compile(r'\{%-?\s*macro\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(')
TOKEN = re.compile(r'\{%-?\s*(macro\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(|endmacro)')
CALL = re.compile(r'\b([A-Z][A-Z0-9_]*)\s*\(')


def macros(text):
    """{name: its text}, nested macros included (a nested one is also part of the macro around it)"""
    out, stack = {}, []
    for m in TOKEN.finditer(text):
        if m.group(2):
            stack.append((m.group(2), m.start()))
        elif stack:
            name, start = stack.pop()
            end = text.index('%}', m.start()) + 2
            out[name] = text[start:end]
    return out


def spec_text(spec):
    """the payloads a spec draws with (its own macros are in them)"""
    sp = importlib.util.spec_from_file_location(spec, SRC / 'specs' / f'{spec}.py')
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return '\n'.join(m.PAYLOADS)


def reach(text, known):
    """every known macro a text calls, directly or through the macros it calls"""
    seen, todo = set(), [text]
    while todo:
        for n in CALL.findall(todo.pop()):
            if n in known and n not in seen:
                seen.add(n)
                todo.append(known[n])
    return seen


def changed(ref):
    """the macros whose text differs from the git ref, in the kit and in the shared spec pieces"""
    out = set()
    files = ['ds_macros.jinja'] + sorted(f'specs/{f.name}' for f in (SRC / 'specs').glob('_*.py'))
    for rel in files:
        now = macros((SRC / rel).read_text())
        r = subprocess.run(['git', 'show', f'{ref}:src/{rel}'], capture_output=True, text=True, cwd=SRC)
        old = macros(r.stdout) if r.returncode == 0 else {}
        out |= {n for n in set(now) | set(old) if now.get(n) != old.get(n)}
    return out


def main():
    args = sys.argv[1:]
    if not args:
        sys.exit(__doc__)
    if args[0] == '--diff':
        targets = changed(args[1] if len(args) > 1 else 'HEAD')
        if not targets:
            print('no macro differs')
            return
    else:
        targets = set(args)
    from layouts import layouts, registry
    kit = macros((SRC / 'ds_macros.jinja').read_text())
    unknown = sorted(t for t in targets if t not in kit and not any(t in macros((SRC / 'specs' / f.name).read_text()) for f in (SRC / 'specs').glob('_*.py')))
    names = {k: v['name'] for k, v in registry()['pages'].items()}
    by_page = {}
    for lay in layouts():
        text = spec_text(lay['spec'])
        known = dict(kit, **macros(text))
        hit = sorted(reach(text, known) & targets)
        if hit:
            by_page.setdefault(names.get(lay['page'], lay['page']), []).append((lay['key'], hit))
    print('macros: ' + ', '.join(sorted(targets)) + (f"   (no such macro: {', '.join(unknown)})" if unknown else ''))
    if not by_page:
        print('no layout draws with them')
    for page in sorted(by_page):
        keys = by_page[page]
        same = len({tuple(h) for _, h in keys}) == 1
        print(f"{page}: {', '.join(k for k, _ in keys)}" + (f"   ({', '.join(keys[0][1])})" if same and len(targets) > 1 else ''))
        if not same:
            for k, h in keys:
                print(f"    {k}: {', '.join(h)}")
    print(f'{sum(len(v) for v in by_page.values())} layouts on {len(by_page)} pages')


if __name__ == '__main__':
    main()
