import os, sys; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import harness
from jinja2 import meta
class SC: STATES={}; NOW=None
env=harness.make_env(SC)
def fv(t): return set(meta.find_undeclared_variables(env.parse(t)))
PROVIDED={'f12','f12b','f16','f16b','f12r','f16r','f21','f21b','fhero','font_file','ds_ink','color','EP_PRIMARY','ds_wtxt','wx','forecast_entity','ds_fd','ds_fh','ds_devs','font_dir','EP_TK','EP_TIER','EP_SPACE','EP_STROKE','EP_ICON','EP_CHART','FONT'}
def needs(path):
    bp=harness.load_bp(path)
    top=bp.get('variables') or {}
    actvars={}
    payloads=[]
    def walk(steps):
        for st in steps:
            if 'variables' in st: actvars.update(st['variables'])
            if st.get('action')=='opendisplay.drawcustom': payloads.append(st['data']['payload'])
            for o in st.get('choose',[]): walk(o['sequence'])
            if 'default' in st: walk(st['default'])
            if 'then' in st: walk(st['then'])
            if 'else' in st: walk(st['else'])
            if 'sequence' in st and 'choose' not in st: walk(st['sequence'])
    walk(bp.get('action') or bp.get('actions'))
    want=set().union(*[fv(p) for p in payloads])
    if 'wx' in actvars: want|=fv(actvars['wx'])
    out={}
    for n in sorted(want-PROVIDED):
        if n in top: out[n]='input' if isinstance(top[n],harness.Input) else 'top-template'
        elif n in actvars: out[n]='action-var'
    return out
if __name__ == "__main__":
  for p in sys.argv[1:]:
    print(p.split('/')[-1], needs(p))
