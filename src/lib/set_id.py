#!/usr/bin/env python3
"""The set id of a built package (design system: Blueprint mechanics, One set).

usage: set_id.py PKG

The id is six letters taken from the SHA-256 of the four templates as built (with the placeholder still in them), so it
changes when the templates change and only then. Letters only: Home Assistant turns a text that reads as a number into
a number (an all-digit id reached the templates as an integer and never equalled their text), and letters can't. It replaces the placeholder in ep_design.jinja and in every
blueprint of the package: a blueprint and templates with the same id are from the same set.
"""
import glob, hashlib, pathlib, sys

MARK = '@@EPSET@@'


def main(pkg):
    pkg = pathlib.Path(pkg)
    tpl = sorted((pkg / 'custom_templates').glob('ep_*.jinja'))
    h = hashlib.sha256()
    for f in tpl:
        h.update(f.name.encode()); h.update(f.read_bytes())
    sid = ''.join('abcdefghijklmnopqrstuvwxyz'[b % 26] for b in h.digest()[:6])
    assert sid.isalpha() and len(sid) == 6, sid
    n = 0
    for f in tpl + [pathlib.Path(p) for p in sorted(glob.glob(str(pkg / 'epaper-*.yaml')))]:
        t = f.read_text(encoding='utf-8')
        if MARK in t:
            f.write_text(t.replace(MARK, sid), encoding='utf-8'); n += 1
    if not n:
        sys.exit('set_id: no placeholder found (already filled in?)')
    print(f'set id {sid} in {n} files')


if __name__ == '__main__':
    main(sys.argv[1])
