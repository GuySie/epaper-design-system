# the widest readings: -12.5 °C flagged low, the widest detail values
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/vd.py').read())
STATS_RESPONSE = {'statistics': {E: series(24, lambda x: -8.0 - 4.6 * math.exp(-((x - 0.95) / 0.2) ** 2), 0.2)}}
STATES[E]['state'] = '-12.5'
STATES[E]['attributes'].update(unit_of_measurement='°C', friendly_name='Freezer room')
STATES['sensor.t']['state'] = '-12.5'
STATES['sensor.h'] = D('1240', 'ppm', 'Living room CO2')
INPUTS.update({'flag_low': True, 'warning_low': -10, 'severe_low': -12, 'icon': 'mdi:thermometer'})
