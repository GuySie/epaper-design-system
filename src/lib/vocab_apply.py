"""Apply lib/vocab.py's rewrite to the comments of the code (Jinja {# #} blocks, Python # lines) — never to strings,
which may have to match upstream text — and to a built package's yamls and README in full.
usage: vocab_apply.py code | vocab_apply.py package DIR"""
import re, sys, glob, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from vocab import rewrite, rewrite_aliases


def rw(t):
    return rewrite_aliases(rewrite(t))

SRC = pathlib.Path(__file__).resolve().parent.parent
CODE = [str(SRC / f) for f in ['ds_macros.jinja', 'lib/ep_tokens.jinja', 'lib/build_lib.py']] + sorted(glob.glob(str(SRC / 'specs' / '*.py')))
JCOM = re.compile(r'\{#.*?#\}', re.S)


def comments_only(text, py):
    text = JCOM.sub(lambda m: rw(m.group(0)), text)
    if py:
        text = '\n'.join((l[:l.index('#')] + rw(l[l.index('#'):])) if re.match(r'^\s*#', l) else l for l in text.split('\n'))
    return text


if __name__ == '__main__':
    n = 0
    if sys.argv[1] == 'code':
        for f in CODE:
            t = open(f).read(); u = comments_only(t, f.endswith('.py'))
            if u != t:
                open(f, 'w').write(u); n += 1; print('rewrote comments in', f)
    else:
        d = sys.argv[2]
        for f in sorted(glob.glob(f'{d}/*.yaml')) + glob.glob(f'{d}/README.md'):
            t = open(f).read(); u = rewrite(t)
            if u != t:
                open(f, 'w').write(u); n += 1
        for f in sorted(glob.glob(f'{d}/custom_templates/*.jinja')):
            t = open(f).read(); u = JCOM.sub(lambda m: rewrite(m.group(0)), t)
            if u != t:
                open(f, 'w').write(u); n += 1
    print(n, 'files changed')
