# an example of what the page is used for (README, lib/pictures.py): in English, on a BWRY panel
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/sv.py').read())
STATES['sensor.holiday'] = S('12', 'days', 'Holiday')
DEVICE_NAMES['sensor.holiday'] = 'Holiday'
INPUTS['entity'] = 'sensor.holiday'
INPUTS.update({'weekday_format': 'en', 'displays': ['dev1']})
MODELS = {'dev1': 'BWRY'}
