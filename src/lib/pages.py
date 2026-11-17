"""The one loader of the page definitions (pages/<page>.yaml) and of what they share (pages/_shared.yaml).

  names()      every page, by file name, in order
  load(page)   a page definition as data, its keys checked
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


def load(page):
    d = copy.deepcopy(_read(page))
    unknown = [k for k in d if k not in KEYS]
    if unknown:
        sys.exit(f'pages/{page}.yaml: unknown key {", ".join(unknown)} (a page definition holds: {", ".join(KEYS)})')
    return d


def shared():
    return copy.deepcopy(_read('_shared'))
