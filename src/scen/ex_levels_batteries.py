# an example of what the page is used for (README, lib/pictures.py): in English, on a BWRY panel
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/lv.py').read())
STATES = {'sensor.b1': S('82', '%', 'Phone'), 'sensor.b2': S('41', '%', 'Tablet'), 'sensor.b3': S('18', '%', 'Front door lock'), 'sensor.b4': S('27', '%', 'Smoke detector')}
DEVICE_NAMES = {e: d['attributes']['friendly_name'] for e, d in STATES.items()}
INPUTS = {'bar_1': 'sensor.b1', 'bar_2': 'sensor.b2', 'bar_3': 'sensor.b3', 'bar_4': 'sensor.b4', 'header_title': 'Batteries', 'flag_low': True, 'warning_low': 30, 'severe_low': 20}
INPUTS.update({'weekday_format': 'en', 'displays': ['dev1']})
MODELS = {'dev1': 'BWRY'}
