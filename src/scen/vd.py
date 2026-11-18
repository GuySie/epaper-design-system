# Value with details: a bedroom's CO2 with the room's climate beside it, thresholds off
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/hg_co2.py').read())
STATS_RESPONSE = {'statistics': {E: series(24, lambda x: 950 + 310 * math.exp(-((x - 0.95) / 0.2) ** 2), 6)}}
STATES[E]['state'] = '1240'
STATES[E]['attributes']['friendly_name'] = 'Bedroom air'
DEVICE_NAMES[E] = 'Bedroom air'
def D(state, unit, name): return {'state': state, 'attributes': dict({'friendly_name': name}, **({'unit_of_measurement': unit} if unit else {})), 'last_updated': NOW - dt.timedelta(minutes=1)}
STATES.update({'sensor.t': D('21.4', '°C', 'Temperature'), 'sensor.h': D('48', '%', 'Humidity'), 'sensor.o': D('12', '°C', 'Outside'), 'binary_sensor.w': D('off', '', 'Window')})
TRANSLATED = {'binary_sensor.w': 'Closed'}
DEVICE_NAMES.update({'sensor.t': 'Temperature', 'sensor.h': 'Humidity', 'sensor.o': 'Outside', 'binary_sensor.w': 'Window'})
INPUTS.update({'detail_1': 'sensor.t', 'detail_2': 'sensor.h', 'detail_3': 'sensor.o', 'detail_4': 'binary_sensor.w', 'icon': 'mdi:molecule-co2'})
