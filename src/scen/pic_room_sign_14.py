# the reference picture of this layout (lib/pictures.py): in English, on a BWRY panel, the room busy
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/rs_busy.py').read())
INPUTS.update({'weekday_format': 'en', 'displays': ['dev1']})
MODELS = {'dev1': 'BWRY'}
