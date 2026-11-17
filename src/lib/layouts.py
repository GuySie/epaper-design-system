#!/usr/bin/env python3
"""The one list of layouts: every page definition's `layouts` (pages/<page>.yaml), one per screen the page is drawn on.

A layout's key is its page and its screen (`weather_27l`), which is also its public name in the templates; its spec is the
file in specs/ that holds its drawing (named after the key); its blueprint's name and file follow from the page's name and
the screen (naming). Everything else that used to list the
layouts by hand reads this: the build's keys and names, the check's blueprint map and canvas sizes, a file's screen, and
the registry's blueprints per page.

usage: layouts.py            print the spec keys, comma-separated (release.sh)
"""
import functools, pathlib, sys

LIB = pathlib.Path(__file__).resolve().parent
SRC = LIB.parent
sys.path.insert(0, str(LIB))


SOURCE = 'https://github.com/GuySie/epaper-design-system/blob/main/blueprints/'
ORIENT = {'L': 'landscape', 'P': 'portrait'}


def naming(page_name, screen_name):
    """a blueprint's name and file from its page and its screen (design system: Blueprint mechanics, Names and files):
    `E-paper <Page> <size>" [landscape|portrait]` and `epaper-blueprint-<size>-<page>[-landscape|-portrait].yaml`; the
    orientation is there for a screen that has both"""
    import re
    size, _, o = screen_name.partition('" ')
    size, o = size.rstrip('"'), ORIENT.get(o.strip(), '')
    slug = re.sub(r'[^a-z0-9]+', '-', page_name.lower()).strip('-')
    return (f'E-paper {page_name} {size}"' + (f' {o}' if o else ''),
            f'epaper-blueprint-{size}-{slug}' + (f'-{o}' if o else '') + '.yaml')


@functools.lru_cache(maxsize=None)
def layouts():
    import pages, yaml
    from derive_tokens import KNOWN, SCREEN_OF
    reg = yaml.safe_load((SRC / 'registry.yaml').read_text(encoding='utf-8'))
    tier_of = {s: t for t, s in SCREEN_OF.items()}
    out, seen = [], {}
    for page in pages.names():
        for scr, lay in (pages.load(page).get('layouts') or {}).items():
            scr = str(scr)
            key = lay.get('key') or f"{page.replace('-', '_')}_{scr}"
            # a page definition gives a layout only its drawing (spec); a mock-up names itself (lib/preview.py)
            title, bp = naming((reg['pages'].get(page) or {}).get('name', page), reg['screen_names'].get(scr, scr))
            title, bp = lay.get('name') or title, lay.get('blueprint') or bp
            public = lay.get('layout') or key
            for what, v in (('key', key), ('spec', lay['spec']), ('blueprint', bp), ('layout', public)):
                if seen.setdefault((what, v), key) != key:
                    sys.exit(f'pages/{page}.yaml: {what} {v} is used by two layouts')
            out.append({'key': key, 'page': page, 'screen': scr, 'spec': lay['spec'], 'name': public, 'title': title,
                        'blueprint': bp, 'source_url': lay.get('source_url') or SOURCE + bp,
                        'tier': tier_of[scr], 'canvas': tuple(KNOWN[tier_of[scr]][:2])})
    return tuple(out)


def registry():
    """registry.yaml with each page's blueprints (layout keys) filled in from the page definitions"""
    import yaml
    r = yaml.safe_load((SRC / 'registry.yaml').read_text(encoding='utf-8'))
    for page, pg in r['pages'].items():
        own = [l['key'] for l in layouts() if l['page'] == page]
        if own or pg.get('blueprints'):
            pg['blueprints'] = own + [b for b in (pg.get('blueprints') or []) if b not in own]
    return r


if __name__ == '__main__':
    print(','.join(sorted(l['spec'] for l in layouts())))
