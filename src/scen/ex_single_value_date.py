# an example of what the page is used for (README, lib/pictures.py): in English, on a BWRY panel
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/sv.py').read())
STATES['sensor.day'] = S('14', '', 'August')
STATES['sensor.weekday'] = S('Saturday', '', 'Weekday')
DEVICE_NAMES.update({'sensor.day': 'August', 'sensor.weekday': 'Weekday'})
INPUTS.update({'entity': 'sensor.day', 'secondary_entity': 'sensor.weekday'})
INPUTS.update({'weekday_format': 'en', 'displays': ['dev1']})
MODELS = {'dev1': 'BWRY'}
