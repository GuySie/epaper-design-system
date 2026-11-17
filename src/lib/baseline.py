"""Reference renders: what a build draws, kept to compare a later build with.

  baseline.py save PKG NAME    render every check case (and the weather extras) of every layout from the package PKG
                               (blueprints + custom_templates) into baseline/NAME/: one PNG and one payload JSON per case
  baseline.py cmp  PKG NAME    render the same cases from PKG and compare with baseline/NAME; exit 1 on a difference
      DIFF   a render or its payload differs          NEW    a case the reference doesn't have (listed, never a failure)
      GONE   a reference render whose case no longer exists (only when every layout is compared)
    The renders that differ or are new are kept in baseline/NAME.new/ to look at.

  EP_KEYS=key,...     only these layouts (while building; a release compares all)
  EP_EXPECT=key,...   the layouts a change is meant to alter: their differences are listed as expected and don't fail
  EP_RENDERS=DIR      renders check.py kept from the same package: reused, so a case is rendered once

A refactor must report 0 differences. An intended change names its layouts in EP_EXPECT, is logged in work/decisions.md and
the reference is saved again.
"""
import atexit, sys, os, json, io, contextlib, shutil, tempfile
import numpy as np
from PIL import Image
BP = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BP)
sys.path.insert(0, os.path.join(BP, 'lib'))
import harness
from pixcmp_cases import B, CASES, SIZES, WEATHER_EXTRA, EXTRA_KEYS

ROOT = os.path.join(BP, 'baseline')
TMP = tempfile.mkdtemp(prefix='epaper_baseline_')      # this run's scratch folder, removed when the run ends
atexit.register(shutil.rmtree, TMP, True)


def cases():
    for key in B:
        scens = [c[0] for c in CASES if c[1] == key]
        if key in EXTRA_KEYS:
            scens += [s for s in WEATHER_EXTRA if s not in scens]
        for s in dict.fromkeys(scens):
            yield key, s


def render(slim, key, s, png):
    W, H = SIZES[key]
    f = f'{TMP}/{key}_{s}.py'
    open(f, 'w').write(f"exec(open('{BP}/scen/{s}.py').read())\nSIZE=({W},{H})\n")
    os.environ['EP_CT'] = f'{slim}/custom_templates'
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            p = harness.run(f'{slim}/{B[key]}', f, png)
        return json.dumps(p, ensure_ascii=False, sort_keys=True)
    except SystemExit as e:
        return 'ERROR ' + str(e)[:300]
    except Exception as e:
        return 'EXC ' + repr(e)[:300]


def keys_of(var):
    """the layout keys an environment variable names; one that is no layout stops the run"""
    ks = [k for k in os.environ.get(var, '').split(',') if k]
    unknown = [k for k in ks if k not in B]
    if unknown:
        sys.exit(f'{var}: no layout {", ".join(unknown)} (layouts: {", ".join(sorted(B))})')
    return ks


def main():
    if len(sys.argv) != 4 or sys.argv[1] not in ('save', 'cmp'):
        sys.exit(__doc__)
    mode, slim, name = sys.argv[1:4]
    d = f'{ROOT}/{name}'
    if mode == 'cmp' and not os.path.isdir(d):
        sys.exit(f'no reference {name} in {ROOT}')
    os.makedirs(d, exist_ok=True)
    only, expect = keys_of('EP_KEYS'), keys_of('EP_EXPECT')
    kept = os.environ.get('EP_RENDERS')            # check.py already rendered these cases from the same package: reuse them
    new = f'{d}.new'                               # cmp: the renders that differ, to look at
    if mode == 'cmp':
        shutil.rmtree(new, ignore_errors=True)
    n = bad = 0
    report, tags = [], set()
    for key, s in cases():
        if only and key not in only:
            continue
        n += 1
        tag = f'{key}__{s}'
        tags.add(tag)
        png = f'{d}/{tag}.png' if mode == 'save' else f'{TMP}/{tag}.png'
        if kept and os.path.exists(f'{kept}/{tag}.json'):
            shutil.copy(f'{kept}/{tag}.png', png)
            p = open(f'{kept}/{tag}.json').read()
        else:
            p = render(slim, key, s, png)
        if mode == 'save':
            open(f'{d}/{tag}.json', 'w').write(p)
            continue
        msg = []
        if not os.path.exists(f'{d}/{tag}.json'):
            report.append(f'NEW  {tag}: not in the reference')
        else:
            if p != open(f'{d}/{tag}.json').read():
                msg.append('payload')
            if not p.startswith(('ERROR', 'EXC')) and os.path.exists(f'{d}/{tag}.png'):
                a = np.array(Image.open(f'{d}/{tag}.png').convert('RGB')); b = np.array(Image.open(png).convert('RGB'))
                k = int((a != b).any(2).sum()) if a.shape == b.shape else -1
                if k:
                    ys = np.where((a != b).any(2))[0] if k > 0 else [0]
                    msg.append(f'{k} px rows {min(ys)}-{max(ys)}')
            if not msg:
                continue
            ok = key in expect
            bad += not ok
            report.append(('EXPECTED ' if ok else '') + f'DIFF {tag}: ' + ', '.join(msg))
        if os.path.exists(png):
            os.makedirs(new, exist_ok=True)
            shutil.copy(png, f'{new}/{tag}.png')
    if mode == 'save':
        for f in os.listdir(d):                    # a reference holds this build's cases only
            if '__' in f and f.rsplit('.', 1)[0] not in tags and not only:
                os.remove(f'{d}/{f}')
        errs = sum(1 for f in os.listdir(d) if f.endswith('.json') and open(f'{d}/{f}').read().startswith(('ERROR', 'EXC')))
        print(f'saved {n} cases to {d} ({errs} expected error/edge renders)')
        return
    if not only:                                   # every layout compared: a reference render without a case is reported
        for f in sorted(os.listdir(d)):
            tag = f[:-5]
            if f.endswith('.json') and '__' in f and tag not in tags:
                ok = tag.split('__')[0] in expect
                bad += not ok
                report.append(('EXPECTED ' if ok else '') + f'GONE {tag}: in the reference, no such case now')
    for r in report:
        print(r)
    print(f'{n} cases, {bad} differ' + (f'; the renders that differ or are new: {new}' if os.path.isdir(new) else ''))
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
