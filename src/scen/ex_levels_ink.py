# an example of what the page is used for (README, lib/pictures.py): in English, on a BWRY panel
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/lv.py').read())
STATES = {'sensor.k': S('62', '%', 'Black'), 'sensor.c': S('35', '%', 'Cyan'), 'sensor.m': S('48', '%', 'Magenta'), 'sensor.y': S('9', '%', 'Yellow')}
DEVICE_NAMES = {e: d['attributes']['friendly_name'] for e, d in STATES.items()}
INPUTS = {'bar_1': 'sensor.k', 'bar_2': 'sensor.c', 'bar_3': 'sensor.m', 'bar_4': 'sensor.y', 'header_title': 'Printer ink', 'flag_low': True, 'warning_low': 20, 'severe_low': 10}
INPUTS.update({'weekday_format': 'en', 'displays': ['dev1']})
MODELS = {'dev1': 'BWRY'}
