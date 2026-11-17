# the reference picture of this layout (lib/pictures.py): its ordinary state, in English, on a BWRY panel
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/a41_6.py').read())
INPUTS['weekday_format'] = 'en'
INPUTS['displays'] = ['dev1']
MODELS = {'dev1': 'BWRY'}
