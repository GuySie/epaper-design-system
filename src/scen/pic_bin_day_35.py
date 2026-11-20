# the reference picture of this layout (lib/pictures.py): in English, on a BWRY panel, a bin collected tomorrow
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/bd_long.py').read())
INPUTS.update({'weekday_format': 'en', 'displays': ['dev1']})
MODELS = {'dev1': 'BWRY'}
