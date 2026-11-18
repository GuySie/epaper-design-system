# whole numbers over 24 hours: a CO2 sensor
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/hg.py').read())
STATS_RESPONSE = {'statistics': {E: series(24, lambda x: 520 + 1150 * math.exp(-((x - 0.45) / 0.16) ** 2), 6)}}
STATES[E]['state'] = '640'
STATES[E]['attributes'].update(unit_of_measurement='ppm', friendly_name='Bedroom CO2')
DEVICE_NAMES[E] = 'Bedroom CO2'
INPUTS['hours'] = '24'
