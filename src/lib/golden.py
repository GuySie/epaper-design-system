"""The blueprint package as data, to compare two builds when a change must not alter behaviour.

  golden.py save PKG NAME   write baseline/NAME/golden.json: per blueprint its inputs (section, order, default, selector),
                            its description, and everything else (triggers, conditions, variables, actions) as normalised data
  golden.py cmp  PKG NAME   compare another package with it; prints each difference, exit 1 when there is one

Formatting and comments never count: the YAML is loaded, and !input references become {'!input': name}.
"""
import sys, os, glob, json
import yaml

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'baseline')


class Loader(yaml.SafeLoader):
    pass


Loader.add_constructor('!input', lambda l, n: {'!input': l.construct_scalar(n)})


def inputs(inp):
    out = []
    for k, v in (inp or {}).items():
        if isinstance(v, dict) and 'input' in v and 'selector' not in v:
            for n, d in (v['input'] or {}).items():
                out.append({'section': k, 'section_name': v.get('name'), 'collapsed': bool(v.get('collapsed')),
                            'name': n, 'label': d.get('name'), 'default': d.get('default', '<required>'),
                            'selector': d.get('selector'), 'help': d.get('description')})
        else:
            out.append({'section': None, 'name': k, 'label': v.get('name'), 'default': v.get('default', '<required>'),
                        'selector': v.get('selector'), 'help': v.get('description')})
    return out


def snapshot(pkg):
    snap = {}
    for f in sorted(glob.glob(f'{pkg}/epaper-*.yaml')):
        d = yaml.load(open(f, encoding='utf-8'), Loader=Loader)
        bp = d.pop('blueprint')
        snap[os.path.basename(f)] = {
            'name': bp.get('name'), 'description': bp.get('description'), 'source_url': bp.get('source_url'),
            'inputs': inputs(bp.get('input')), 'body': d}
    return snap


def diff(a, b, path=''):
    if type(a) != type(b):
        yield f'{path}: {json.dumps(a, ensure_ascii=False)[:120]} -> {json.dumps(b, ensure_ascii=False)[:120]}'
    elif isinstance(a, dict):
        for k in list(a) + [k for k in b if k not in a]:
            if k not in b:
                yield f'{path}/{k}: removed'
            elif k not in a:
                yield f'{path}/{k}: added'
            else:
                yield from diff(a[k], b[k], f'{path}/{k}')
    elif isinstance(a, list):
        if len(a) != len(b):
            yield f'{path}: {len(a)} items -> {len(b)}'
        for i, (x, y) in enumerate(zip(a, b)):
            yield from diff(x, y, f'{path}[{i}]')
    elif a != b:
        yield f'{path}: {json.dumps(a, ensure_ascii=False)[:120]} -> {json.dumps(b, ensure_ascii=False)[:120]}'


def main():
    mode, pkg, name = sys.argv[1:4]
    p = f'{ROOT}/{name}/golden.json'
    if mode == 'save':
        os.makedirs(os.path.dirname(p), exist_ok=True)
        if os.path.exists(p):
            os.replace(p, p + '.old')      # overwrite, never delete
        json.dump(snapshot(pkg), open(p, 'w'), ensure_ascii=False, indent=1, sort_keys=True)
        print(f'saved {p}')
        return 0
    ref, now = json.load(open(p)), json.loads(json.dumps(snapshot(pkg)))
    n = 0
    for k in sorted(set(ref) | set(now)):
        for line in (['missing'] if k not in now else ['new'] if k not in ref else diff(ref[k], now[k])):
            n += 1
            print(f'{k}{line if line.startswith("/") else ": " + line}')
    print(f'{len(now)} blueprints, {n} differences')
    return 1 if n else 0


if __name__ == '__main__':
    sys.exit(main())
