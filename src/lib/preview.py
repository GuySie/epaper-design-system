#!/usr/bin/env python3
"""Mock-ups without a release (CLAUDE.md, How a change goes, step 4): render a draft layout with the real macros and tokens.

  preview.py --page PAGE --screen SCREEN --spec DRAFT.py SCEN [SCEN ...]
             [--panel W H Wmm Hmm]                a screen that has no tier yet: its tokens are derived from these panel facts
             [--fit-hero SCEN,...]                measure type.heroShared on these widest readings (hero beside other content)
             [--fit-glance SCEN,...]              measure type.heroAlone on these ordinary readings (hero on its own)
             [--fit-strips]                       measure the strip icons on the scenarios given
             [--page-file DRAFT.yaml]             a page that does not exist yet: its draft page definition
             [--out DIR]                          default: ../work/mockups/<draft name>
A patch.py next to the draft, when there is one, adjusts the copy where the build can't yet supply the draft's data.

Everything happens in a temporary copy of src/: the sources, the tokens and the references are never touched, nothing is
checked or released. The draft spec (and any helper .py next to it) goes into the copy as the layout of PAGE on SCREEN,
only that blueprint is built, and each scenario (a name in src/scen, or a .py next to the draft) is drawn at the screen's
canvas size. On an existing screen the current tokens are used; on a new one (--panel) the derived tokens come from the
panel facts and the measured ones from a quick fit on the mock-up's own scenarios, marked as provisional. The renders and a
sheet headed "MOCK-UP, NOT CHECKED" go to the output folder.
"""
import argparse, contextlib, io, os, pathlib, shutil, subprocess, sys, tempfile
LIB = pathlib.Path(__file__).resolve().parent
SRC = LIB.parent


def patch(path, text):
    path.write_text(path.read_text() + '\n' + text + '\n')


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--page', required=True)
    ap.add_argument('--page-file', help='a draft page definition (a page that does not exist yet)')
    ap.add_argument('--screen', required=True)
    ap.add_argument('--spec', required=True)
    ap.add_argument('--panel', nargs=4, type=float)
    ap.add_argument('--fit-hero', default='')
    ap.add_argument('--fit-glance', default='')
    ap.add_argument('--fit-strips', action='store_true')
    ap.add_argument('--out')
    ap.add_argument('--keep', action='store_true', help='keep the temporary copy (to inspect a draft)')
    ap.add_argument('scen', nargs='+')
    a = ap.parse_args()
    draft = pathlib.Path(a.spec).resolve()
    stem = draft.stem
    out = pathlib.Path(a.out or SRC.parent / 'work' / 'mockups' / stem).resolve()
    out.mkdir(parents=True, exist_ok=True)

    tmp = pathlib.Path(tempfile.mkdtemp(prefix='preview_'))
    T = tmp / 'src'
    shutil.copytree(SRC, T, ignore=shutil.ignore_patterns('baseline', 'build', '__pycache__'))
    sys.path[:0] = [str(T / 'lib'), str(T)]
    import pageyaml
    from derive_tokens import KNOWN, SCREEN_OF, tier_key

    # the draft layout, on PAGE at SCREEN; only that page and that screen are built
    name, layout = f'mock_{stem}', f'mock_{stem}'
    for f in draft.parent.glob('*.py'):
        shutil.copy(f, T / 'specs' / (f'{name}.py' if f == draft else f.name))
    bp = f'epaper-blueprint-mock-{stem}.yaml'
    pf = T / 'pages' / f'{a.page}.yaml'
    if a.page_file:
        shutil.copy(a.page_file, pf)
    page = pageyaml.load(pf.read_text())
    lay = dict((page.get('layouts') or {}).get(a.screen) or next(iter((page.get('layouts') or {}).values()), {}))
    lay.update(spec=name, key='mock', layout=layout, blueprint=bp, name=f'Mock-up {stem}')      # lib/layouts.py lists it
    lay.pop('source_url', None)
    page['layouts'] = {a.screen: lay}
    pf.write_text(pageyaml.dump(page))
    for f in (T / 'pages').glob('[!_]*.yaml'):
        if f != pf:
            f.unlink()

    # the screen: an existing one, or a new tier from its panel facts
    tier_of = {v: k for k, v in SCREEN_OF.items()}
    if a.panel:
        W, H = int(a.panel[0]), int(a.panel[1])
        tier = tier_key(W, H, a.panel[2], a.panel[3])
        patch(T / 'lib' / 'derive_tokens.py', f"KNOWN[{tier!r}] = ({W}, {H}, {a.panel[2]}, {a.panel[3]})\nSCREEN_OF[{tier!r}] = {a.screen!r}")
        reg = T / 'registry.yaml'
        reg.write_text(reg.read_text().replace("screen_names: {", f"screen_names: {{'{a.screen}': 'mock-up {W} x {H}', ", 1))
        sh = T / 'pages' / '_shared.yaml'
        d = pageyaml.load(sh.read_text())
        d['screens'][a.screen] = f'{W} x {H} devices (mock-up).'
        d['screen_facts'][a.screen] = {'size': f'{W} x {H}', 'native': f'This panel is {W} x {H}'}
        sh.write_text(pageyaml.dump(d))
    else:
        tier = tier_of[a.screen]
        W, H = KNOWN[tier][:2]
    # the registry knows which page the mock-up blueprint belongs to (the shared parts give it that page's texts)
    import yaml
    rf = T / 'registry.yaml'
    reg = yaml.safe_load(rf.read_text())
    pg = reg['pages'].setdefault(a.page, {'name': page.get('page', a.page), 'uses': 'hero-dashboard/module', 'status': 'mock'})
    rf.write_text(yaml.safe_dump(reg, allow_unicode=True, sort_keys=False))

    def scen_file(s):
        f = draft.parent / f'{s}.py'
        return f if f.exists() else T / 'scen' / f'{s}.py'
    for s in a.scen + [x for x in (a.fit_hero + ',' + a.fit_glance).split(',') if x]:
        if scen_file(s).parent == draft.parent:
            shutil.copy(scen_file(s), T / 'scen' / f'{s}.py')
        f = T / 'scen' / f'{s}.py'                 # drawn at the mock-up screen's size, in the fit too (the copy only)
        f.write_text(f.read_text() + f'\nSIZE = ({W}, {H})\n')

    # a draft may adjust the copy where the build can't yet do what it needs (data plumbing, never drawing): patch.py next to
    # the draft gets the copy's src folder; what it changes is the build's work in step 6
    hook = draft.parent / 'patch.py'
    if hook.exists():
        ns = {'T': T, 'pageyaml': pageyaml}
        exec(hook.read_text(), ns)

    # tokens: kept on an existing screen; derived and quickly fitted on a new one (or when a fit is asked for)
    env = dict(os.environ, EP_ROOT=str(T), EP_REFIT='1', PYTHONPATH='')
    provisional = []
    if a.panel or a.fit_hero or a.fit_glance or a.fit_strips:
        fit = [(s, 'C') for s in a.fit_hero.split(',') if s]
        glance = [s for s in a.fit_glance.split(',') if s]
        patch(T / 'lib' / 'layout_fit.py', f"FIT = {{'mock': {fit!r}}} if {bool(fit)} else {{}}\n"
              f"STRIP = ['mock'] if {a.fit_strips} else []\nGLANCE = {{'mock': {glance!r}}} if {bool(glance)} else {{}}")
        patch(T / 'lib' / 'pixcmp_cases.py', 'CASES = ' + repr([(s, 'mock', 'C', 'free') for s in a.scen]))
        r = subprocess.run([sys.executable, 'lib/gen_tokens.py', name], cwd=T, env=env, capture_output=True, text=True)
        if r.returncode:
            sys.exit(f'the quick fit failed (the tokens it needs can\'t be measured on these scenarios):\n{r.stdout[-1500:]}{r.stderr[-1500:]}')
        provisional = [l for l in r.stdout.splitlines() if l.startswith('mock')]

    else:
        # no fit asked for: the measured tokens are per layout, so the mock-up takes those of the layout it replaces (the
        # page's layout on this screen); a layout that doesn't exist yet has none and needs a fit
        import re
        own = f"{a.page.replace('-', '_')}_{a.screen}"
        tk = T / 'lib' / 'ep_tokens.jinja'
        src = tk.read_text()
        m = re.search(r"\n  '%s': \{\n.*?\n  \}" % re.escape(own), src[src.index('EP_LAYOUT'):], re.S)
        if not m:
            sys.exit(f'{own} is no layout yet, so it has no measured tokens: pass --fit-hero, --fit-glance or --fit-strips')
        i = src.index('EP_LAYOUT') + m.start()
        tk.write_text(src[:i] + m.group(0).replace(f"'{own}'", f"'{layout}'", 1) + ',' + src[i:])
        provisional = [f'measured tokens: those of {own}']

    # build only this blueprint, then draw each scenario at the screen's canvas size
    pkg = tmp / 'pkg'
    for cmd in (['lib/build_lib.py', str(pkg), name], ['lib/generate.py', str(pkg)], ['lib/inputs_std.py', str(pkg)],
                ['lib/shared.py', str(pkg)], ['lib/vocab_apply.py', 'package', str(pkg)], ['lib/set_id.py', str(pkg)]):
        r = subprocess.run([sys.executable, *cmd], cwd=T, env=env, capture_output=True, text=True)
        if r.returncode:
            sys.exit(f'building the mock-up failed at {cmd[0]}:\n{r.stdout[-1500:]}{r.stderr[-1500:]}')
    os.environ.update(EP_ROOT=str(T), EP_CT=str(pkg / 'custom_templates'))
    import harness
    from PIL import Image, ImageDraw, ImageFont
    pngs = []
    for s in a.scen:
        f = tmp / f'scen_{s}.py'
        f.write_text(f"exec(open({str(T / 'scen' / f'{s}.py')!r}).read())\nSIZE=({W},{H})\n")
        png = out / f'{s}.png'
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                harness.run(str(pkg / bp), str(f), str(png))
            pngs.append((s, png))
        except (SystemExit, Exception) as e:
            print(f'{s}: not drawn: {e}')

    # the sheet: the label, what it is, and the renders side by side
    ims = [(s, Image.open(p).convert('RGB')) for s, p in pngs]
    if ims:
        font = ImageFont.truetype(str(SRC / 'fonts' / 'TRMNL16-Bold.ttf'), 16)
        head = [f'MOCK-UP, NOT CHECKED: {stem} on {a.page}, screen {a.screen} ({tier}, {W} x {H})']
        head += [(l if l.startswith('measured') else f'provisional: {l}') for l in provisional] or ['tokens: the current ones for this tier']
        gap, top = 16, 24 * len(head) + 16
        sheet = Image.new('RGB', (sum(i.width for _, i in ims) + gap * (len(ims) + 1),
                                  top + max(i.height for _, i in ims) + 40), (200, 200, 200))
        dr = ImageDraw.Draw(sheet)
        for n, line in enumerate(head):
            dr.text((gap, 8 + 24 * n), line[:160], fill='black', font=font)
        x = gap
        for s, im in ims:
            sheet.paste(im, (x, top)); dr.text((x, top + im.height + 10), s, fill='black', font=font); x += im.width + gap
        sheet.save(out / 'sheet.png')
        print(f'{out / "sheet.png"}')
    if a.keep:
        print(f'kept: {tmp}')
    else:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == '__main__':
    main()
