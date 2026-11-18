# the reference picture of this layout (lib/pictures.py): in English, on a BWRY panel, high and low thresholds on
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/hg_both.py').read())
INPUTS.update({'weekday_format': 'en', 'displays': ['dev1']})
MODELS = {'dev1': 'BWRY'}
