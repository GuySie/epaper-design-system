# the reference picture of this layout (lib/pictures.py): in English, on a BWRY panel, the number at severe
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/vd_sev.py').read())
INPUTS.update({'weekday_format': 'en', 'displays': ['dev1']})
MODELS = {'dev1': 'BWRY'}
