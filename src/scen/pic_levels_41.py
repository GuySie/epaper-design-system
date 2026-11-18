# the reference picture of this layout (lib/pictures.py): in English, on a BWRY panel, a row at severe and one at warning
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/lv_sev.py').read())
INPUTS.update({'weekday_format': 'en', 'displays': ['dev1']})
MODELS = {'dev1': 'BWRY'}
