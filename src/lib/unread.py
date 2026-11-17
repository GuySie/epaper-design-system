"""What a blueprint carries but nothing reads.

  unread.py PKG    exit 1 when a built blueprint in PKG has an input nothing reads, or a page definition has a text
                   key or a data key nothing reads

  input      an input no trigger, condition or action uses, and no variable that reaches one
  text key   a key of a page's `texts` that no page definition, spec or macro names
  data key   a key of a dictionary built in a page's `data` that nothing reads as `.key`, `['key']` or `attribute='key'`

The text and data checks go by name across all sources, so they miss a key another page happens to read; they never
report one that is read.
"""
import glob, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pageyaml, pages
from jinja2 import Environment, meta

SRC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV = Environment(extensions=['jinja2.ext.do', 'jinja2.ext.loopcontrols'])
LANGS = {'en', 'de', 'nl', 'fr', 'es', 'pl', 'hr', 'sv'}


def names(text):
    """the variables a template reads; every word of it when it doesn't parse as plain Jinja"""
    try:
        return set(meta.find_undeclared_variables(ENV.parse(text)))
    except Exception:
        return set(re.findall(r'[A-Za-z_][A-Za-z_0-9]*', text))


def unread_inputs(path):
    bp = pageyaml.load(open(path).read())
    inputs, variables, used_in, used_var = set(), {}, set(), set()

    def collect(d):
        for k, v in d.items():
            if isinstance(v, dict) and isinstance(v.get('input'), dict) and 'selector' not in v:
                collect(v['input'])           # a section
            else:
                inputs.add(k)

    def scan(node):
        if isinstance(node, pageyaml.Input):
            used_in.add(node['!input'])
        elif isinstance(node, dict):
            for k, v in node.items():
                if k == 'variables' and isinstance(v, dict):
                    for n, val in v.items():
                        variables.setdefault(n, []).append(val)
                else:
                    scan(v)
        elif isinstance(node, list):
            for x in node:
                scan(x)
        elif isinstance(node, str) and ('{{' in node or '{%' in node):
            used_var.update(names(node))

    def reads(val, ins, vs):
        if isinstance(val, pageyaml.Input):
            ins.add(val['!input'])
        elif isinstance(val, dict):
            for x in val.values():
                reads(x, ins, vs)
        elif isinstance(val, list):
            for x in val:
                reads(x, ins, vs)
        elif isinstance(val, str):
            vs.update(names(val))

    collect(bp['blueprint']['input'])
    scan({k: v for k, v in bp.items() if k != 'blueprint'})
    live = used_var & set(variables)
    todo = list(live)
    while todo:
        for val in variables[todo.pop()]:
            ins, vs = set(), set()
            reads(val, ins, vs)
            used_in |= ins
            for v in (vs & set(variables)) - live:
                live.add(v)
                todo.append(v)
    return sorted(inputs - used_in)


def sources():
    """every source a key can be read from, the page definitions without their texts"""
    out = []
    for d in [pages.load(n) for n in pages.names()] + [pages.shared()]:
        d.pop('texts', None)
        out.append(pageyaml.dump(d, width=100000))
    for p in sorted(glob.glob(os.path.join(SRC, 'specs', '*.py'))) + [os.path.join(SRC, f) for f in (
            'ds_macros.jinja', 'wx_steps.yaml', 'wx_txt.yaml', 'lib/shared.py', 'lib/generate.py', 'lib/build_lib.py')]:
        out.append(open(p).read())
    return '\n'.join(out)


def main(pkg):
    bad = []
    for p in sorted(glob.glob(os.path.join(pkg, '*.yaml'))):
        for i in unread_inputs(p):
            bad.append(f'{os.path.basename(p)}: input `{i}` is read by nothing')
    text = sources()
    for name in pages.names():
        d = pages.load(name)
        page = name + '.yaml'
        keys = set()
        for lang, v in (d.get('texts') or {}).items():
            if isinstance(v, dict):
                keys |= set(v)
        for k in sorted(keys):
            if not re.search(r"'%s'" % re.escape(k), text):
                bad.append(f'{page}: text key `{k}` is read by nothing')
        data = pageyaml.dump(d.get('data') or {}, width=100000)
        for k in sorted(set(re.findall(r"'([a-z_0-9]+)'\s*:", data)) - LANGS):
            e = re.escape(k)
            if not re.search(r"\.%s\b(?!\s*=[^=])|\[\s*'%s'\s*\]|attribute\s*=\s*'%s'|\(\s*'%s'" % (e, e, e, e), text):
                bad.append(f'{page}: data key `{k}` is read by nothing')
    for b in bad:
        print(b)
    print(f'unread: {len(bad)} problems')
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
