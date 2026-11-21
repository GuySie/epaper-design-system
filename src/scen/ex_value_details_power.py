# an example of what the page is used for (README, lib/pictures.py): in English, on a BWRY panel
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/vd.py').read())
STATS_RESPONSE = {'statistics': {E: series(24, lambda x: 260 + 1900 * math.exp(-((x - 0.78) / 0.05) ** 2) + 900 * math.exp(-((x - 0.33) / 0.03) ** 2), 40)}}
STATES[E]['state'] = '310'
STATES[E]['attributes'].update(unit_of_measurement='W', friendly_name='Power use')
DEVICE_NAMES[E] = 'Power use'
STATES.update({'sensor.t': D('1.8', 'kW', 'Solar'), 'sensor.h': D('82', '%', 'Battery'), 'sensor.o': D('0.2', 'kW', 'From the grid')})
DEVICE_NAMES.update({'sensor.t': 'Solar', 'sensor.h': 'Battery', 'sensor.o': 'From the grid'})
INPUTS.update({'weekday_format': 'en', 'displays': ['dev1']})
MODELS = {'dev1': 'BWRY'}
