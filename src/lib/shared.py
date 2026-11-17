"""The parts every blueprint shares, as one fragment each.

  shared.py PKG          write the fragments into every blueprint in PKG (idempotent)
  shared.py --lint PKG   report every blueprint whose shared parts differ from the fragments; exit 1 when one does

The fragments:
  texts          `language_map` reads its page's texts from ep_i18n.jinja (EP_TXT, built from the page definitions' `texts`);
                 `weekday_short_map` and `months_short_map` read EP_DAYS_SHORT and EP_MONTHS_SHORT
  stale          `ds_stale`: the data is stale when the newest report is older than `stale_after` minutes (0 turns it off)
  drawing        the opendisplay.drawcustom step: white background, no dither, the `rotate` input, the `displays` input
  button flash   the LED step that confirms a button press (two flashes on the pressed device; Medication flashes its
                 own display, the button's device)
  template note  the description's line on installing the design-system templates
"""
import glob, os, re, sys
import yaml
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pixcmp_cases import B

from layouts import registry          # noqa: E402
REG = registry()
PAGE_OF = {B[str(b)]: p for p, pg in REG['pages'].items() for b in (pg.get('blueprints') or []) if str(b) in B}

TEXTS = {'language_map': "\"{%- from 'ep_i18n.jinja' import EP_TXT -%}{{ EP_TXT['PAGE'] }}\"",
         'weekday_short_map': "\"{%- from 'ep_i18n.jinja' import EP_DAYS_SHORT -%}{{ EP_DAYS_SHORT }}\"",
         'months_short_map': "\"{%- from 'ep_i18n.jinja' import EP_MONTHS_SHORT -%}{{ EP_MONTHS_SHORT }}\""}
STALE = ("{{ (stale_after | int(0)) > 0 and (ds_last_ts | float(0)) > 0 and (as_timestamp(now()) - (ds_last_ts | float(0)))"
         " > (stale_after | int(0)) * 60 }}")
DRAW = {'background': 'white', 'dither': 'none', 'rotate': {'!input': 'rotate'}}
FLASH = {'action': 'opendisplay.activate_led', 'continue_on_error': True,
         'data': {'brightness': 16, 'color1': {'!input': 'led_color'}, 'device_id': '{{ device_id(trigger.entity_id) }}',
                  'flash_count1': 2, 'loop_delay1': {'!input': 'led_flash_delay'}, 'repeats': 1}}
FLASH_OWN = {**FLASH, 'data': {**FLASH['data'], 'device_id': {'!input': 'displays'}}}   # Medication: its own display
NOTE = ("- The design-system templates: copy the four `ep_*.jinja` files from the repository's `custom_templates` folder into "
        "`config/custom_templates/`, then run `homeassistant.reload_custom_templates` (or restart Home Assistant). Update them "
        "together with the blueprints.")


class Loader(yaml.SafeLoader):
    pass


Loader.add_constructor('!input', lambda l, n: {'!input': l.construct_scalar(n)})


def var_block(lines, name):
    """(start, end) of a top-level `variables:` entry"""
    v = lines.index('variables:')
    for i in range(v + 1, len(lines)):
        if lines[i].startswith(f'  {name}:'):
            j = i + 1
            while j < len(lines) and (not lines[j].strip() or lines[j].startswith('    ')):
                j += 1
            while j > i + 1 and not lines[j - 1].strip():
                j -= 1
            return i, j
        if lines[i] and not lines[i].startswith((' ', '#')):
            break
    return None


def write(path):
    page = PAGE_OF.get(os.path.basename(path))
    lines = open(path, encoding='utf-8').read().split('\n')
    for name, frag in TEXTS.items():
        r = var_block(lines, name)
        if r:
            lines[r[0]:r[1]] = [f'  {name}: ' + frag.replace('PAGE', page)]
    t = '\n'.join(lines)
    t = re.sub(r'(\n\s+device_id: )"\{\{ displays \}\}"', r'\1!input displays', t)   # Doors & windows: the input itself
    open(path, 'w', encoding='utf-8').write(t)


def steps(st):
    for s in st or []:
        yield s
        for k in ('then', 'else', 'sequence', 'default'):
            if isinstance(s.get(k), list):
                yield from steps(s[k])
        for o in s.get('choose') or []:
            yield from steps(o['sequence'])


def lint(path):
    f = os.path.basename(path)
    d = yaml.load(open(path, encoding='utf-8'), Loader=Loader)
    errs, v = [], d.get('variables') or {}
    for name, frag in TEXTS.items():
        if name in v and v[name] != yaml.safe_load(frag.replace('PAGE', PAGE_OF.get(f, '?'))):
            errs.append(f'{name} is not the shared texts fragment')
    if 'ds_stale' in v and v['ds_stale'].strip() != STALE:
        errs.append('ds_stale is not the shared stale fragment')
    for s in steps(d.get('action') or d.get('actions')):
        if s.get('action') == 'opendisplay.drawcustom':
            if s.get('target') != {'device_id': {'!input': 'displays'}} or {k: s['data'].get(k) for k in DRAW} != DRAW:
                errs.append('a drawing step is not the shared drawing fragment')
        if s.get('action') == 'opendisplay.activate_led' and s not in (FLASH, FLASH_OWN):
            errs.append('an LED step is not the shared button-flash fragment')
    desc = d['blueprint'].get('description') or ''
    if NOTE not in desc:
        errs.append('the template note differs')
    return errs


if __name__ == '__main__':
    if sys.argv[1] == '--lint':
        bad = 0
        for f in sorted(glob.glob(f'{sys.argv[2]}/epaper-*.yaml')):
            for m in lint(f):
                bad += 1
                print(f'{os.path.basename(f)}: {m}')
        print(f'{bad} problems')
        sys.exit(1 if bad else 0)
    for f in sorted(glob.glob(f'{sys.argv[1]}/epaper-*.yaml')):
        write(f)
    print('ok')
