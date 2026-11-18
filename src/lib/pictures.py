#!/usr/bin/env python3
"""The reference pictures: one per blueprint, and one per example of a page (pages/<page>.yaml `examples`), at the panel's own pixels, in English, with a warning and a severe state
visible where the page has thresholds (each picture case, scen/pic_<layout>.py, says what it adds to the ordinary case).

  pictures.py RENDERS    copy each layout's picture case (`pic_<layout>`: its `normal` case in English, on a BWRY panel where the screen has one) from the renders a release kept
                         (EP_RENDERS) to ../docs/images/<blueprint file name>.png, and remove pictures no blueprint has

The README's picture list (`registry.py write`, block `pictures`) names the same files: `picks()` is the one list.
"""
import pathlib, shutil, sys
LIB = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(LIB))
IMAGES = LIB.parent.parent / 'docs' / 'images'


def picks():
    """[(page name, blueprint file, layout key, case)], pages in the registry's order, a page's blueprints by file name"""
    from layouts import registry
    from pixcmp_cases import B
    key_of = {f: k for k, f in B.items()}
    out = []
    for pg in registry()['pages'].values():
        for f in sorted(B[str(b)] for b in (pg.get('blueprints') or []) if str(b) in B):
            out.append((pg['name'], f, key_of[f], f'pic_{key_of[f]}'))
    return out


def example_picks():
    """[(page name, layout key, case, shows, picture file)]: every page's examples (lib/layouts.py `examples`)"""
    from layouts import registry, examples
    name = {k: p['name'] for k, p in registry()['pages'].items()}
    return [(name[pg], key, case, shows, 'example-' + case[3:].replace('_', '-') + '.png') for pg, key, case, shows, _ in examples()]


def main(renders):
    IMAGES.mkdir(parents=True, exist_ok=True)
    want = set()
    for _, f, key, case in picks():
        src = pathlib.Path(renders) / f'{key}__{case}.png'
        if not src.exists():
            sys.exit(f'pictures: no render {src.name} (the release keeps them in EP_RENDERS)')
        dst = IMAGES / (pathlib.Path(f).stem + '.png')
        shutil.copyfile(src, dst)
        want.add(dst.name)
    for _, key, case, _, f in example_picks():
        src = pathlib.Path(renders) / f'{key}__{case}.png'
        if not src.exists():
            sys.exit(f'pictures: no render {src.name} (the release keeps them in EP_RENDERS)')
        shutil.copyfile(src, IMAGES / f)
        want.add(f)
    for old in IMAGES.glob('*.png'):
        if old.name not in want:
            old.unlink()
    print(f'pictures: {len(want)} in ../docs/images')


if __name__ == '__main__':
    main(sys.argv[1])
