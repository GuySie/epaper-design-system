import datetime as dt
TZ = dt.timezone(dt.timedelta(hours=1))
NOW = dt.datetime(2026, 8, 1, 20, 45, tzinfo=TZ)
SIZE = (384, 184)
ents = [('sensor.co2', '1240', 'ppm', 'CO2'), ('sensor.temp', '21.4', '°C', 'Living room temperature'), ('sensor.hum', '48', '%', 'Moisture'),
        ('sensor.pm25', '4', 'µg/m³', 'PM2.5'), ('sensor.lux', 'unavailable', 'lx', 'Light'), ('binary_sensor.door', 'off', '', 'Front door'),
        ('sensor.solar', '2.1', 'kW', 'Solar panels'), ('switch.lamp', 'on', '', 'Living room ceiling lamp')]
STATES = {e: {'state': s, 'attributes': {'unit_of_measurement': u, 'friendly_name': n}} for e, s, u, n in ents}
INPUTS = {f'entity_{i+1}': e for i, (e, *_r) in enumerate(ents)}
INPUTS.update({f'entity_{i}': '' for i in range(len(ents)+1, 13)})
INPUTS['weekday_format'] = 'nl'
