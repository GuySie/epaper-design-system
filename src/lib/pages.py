"""The one loader of the page definitions (pages/<page>.yaml) and of what they share (pages/_shared.yaml).

  names()      every page, by file name, in order
  load(page)   a page definition as data: its `include: <group>` entries replaced by the group they name
               (pages/_shared.yaml, `groups`), its `repeat` entries written out (a list item `repeat: {from, to,
               items}` stands for its items once per number, `{n}` replaced by the number), its keys checked
  shared()     pages/_shared.yaml

Every tool reads the page definitions through here, so a key a page may have is listed once (KEYS) and a misspelt one
stops the build instead of being ignored.
"""
import copy, functools, pathlib, sys
LIB = pathlib.Path(__file__).resolve().parent
PAGES = LIB.parent / 'pages'
sys.path.insert(0, str(LIB))

# what a page definition may hold: its name and description, when it redraws and goes stale, its inputs and which of
# them the drawing is handed (bind, ds_in), its data, its texts, and its layouts (one per screen)
KEYS = ('page', 'description', 'redraw', 'stale', 'inputs', 'bind', 'ds_in', 'data', 'texts', 'layouts')


def names():
    return [f.stem for f in sorted(PAGES.glob('[!_]*.yaml'))]      # by file name, as the layouts have always been listed


@functools.lru_cache(maxsize=None)
def _read(name):
    import pageyaml
    return pageyaml.load((PAGES / f'{name}.yaml').read_text(encoding='utf-8'))


def _numbered(node, n):
    """a repeat's items for one number: `{n}` replaced in every text"""
    if isinstance(node, str):
        return node.replace('{n}', str(n))
    if isinstance(node, list):
        return [_numbered(x, n) for x in node]
    if isinstance(node, dict):
        return type(node)((_numbered(k, n), _numbered(v, n)) for k, v in node.items())
    return node


def _expand(node, groups, page):
    """`include: <group>` resolved: as a list item the group's items take its place, as a mapping key the group's keys do"""
    import pageyaml
    def group(name, kind):
        if name not in groups or not isinstance(groups[name], kind):
            sys.exit(f'pages/{page}.yaml: include {name!r} is not a {"list" if kind is list else "mapping"} group in pages/_shared.yaml')
        return copy.deepcopy(groups[name])
    if isinstance(node, pageyaml.Input):
        return node
    if isinstance(node, list):
        out = []
        for x in node:
            if isinstance(x, dict) and list(x) == ['include']:
                out.extend(_expand(group(x['include'], list), groups, page))
            elif isinstance(x, dict) and list(x) == ['repeat']:
                r = x['repeat']
                for n in range(int(r['from']), int(r['to']) + 1):
                    out.extend(_expand(_numbered(r['items'], n), groups, page))
            else:
                out.append(_expand(x, groups, page))
        return out
    if isinstance(node, dict):
        out = {}
        for k, v in node.items():
            if k == 'include':
                out.update(_expand(group(v, dict), groups, page))
            else:
                out[k] = _expand(v, groups, page)
        return out
    return node


def load(page):
    d = _expand(copy.deepcopy(_read(page)), _read('_shared').get('groups') or {}, page)
    unknown = [k for k in d if k not in KEYS]
    if unknown:
        sys.exit(f'pages/{page}.yaml: unknown key {", ".join(unknown)} (a page definition holds: {", ".join(KEYS)})')
    return d


def shared():
    return copy.deepcopy(_read('_shared'))
