# an example of what the page is used for (README, lib/pictures.py): in English, on a BWRY panel
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/vd.py').read())
STATS_RESPONSE = {'statistics': {E: series(24, lambda x: 11.0 + 5.5 * math.exp(-((x - 0.72) / 0.14) ** 2), 0.2)}}
STATES[E]['state'] = '12.3'
STATES[E]['attributes'].update(unit_of_measurement='°C', friendly_name='Outside')
DEVICE_NAMES[E] = 'Outside'
STATES.update({'sensor.t': D('71', '%', 'Humidity'), 'sensor.h': D('14', 'km/h', 'Wind'), 'sensor.o': D('0.4', 'mm', 'Rain today')})
DEVICE_NAMES.update({'sensor.t': 'Humidity', 'sensor.h': 'Wind', 'sensor.o': 'Rain today'})
INPUTS.update({'weekday_format': 'en', 'displays': ['dev1']})
MODELS = {'dev1': 'BWRY'}
