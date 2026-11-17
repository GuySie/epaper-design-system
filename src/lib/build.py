#!/usr/bin/env python3
"""The build: the whole package (the templates and every blueprint) from the sources, in one place.

  build.py OUT [KEYS] [--no-set-id]    KEYS: the layouts to build, comma-separated (default: every layout)

The steps, in order: the templates (build_lib.py), the blueprints (generate.py), the input scheme (inputs_std.py), the
shared parts (shared.py), the vocabulary in the package (vocab_apply.py), and last the set id (set_id.py: a hash of
the templates as built). release.sh, the token fit (gen_tokens.py, which needs no set id) and the mock-up tool
(preview.py) all build through here.
"""
import pathlib, subprocess, sys
LIB = pathlib.Path(__file__).resolve().parent
SRC = LIB.parent


def build(out, keys=None, set_id=True, env=None):
    if keys is None:
        keys = subprocess.run([sys.executable, 'lib/layouts.py'], cwd=SRC, check=True, capture_output=True, text=True, env=env).stdout.strip()
    steps = [['lib/build_lib.py', str(out), keys], ['lib/generate.py', str(out)], ['lib/inputs_std.py', str(out)],
             ['lib/shared.py', str(out)], ['lib/vocab_apply.py', 'package', str(out)]]
    if set_id:
        steps.append(['lib/set_id.py', str(out)])
    for cmd in steps:
        subprocess.run([sys.executable, *cmd], cwd=SRC, check=True, stdout=subprocess.DEVNULL, env=env)


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if a != '--no-set-id']
    if not args:
        sys.exit(__doc__)
    pathlib.Path(args[0]).mkdir(parents=True, exist_ok=True)
    build(args[0], args[1] if len(args) > 1 else None, set_id='--no-set-id' not in sys.argv)
