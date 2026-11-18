# Single value: a CO2 sensor, 1240 ppm
import datetime as dt
TZ = dt.timezone(dt.timedelta(hours=1))
NOW = dt.datetime(2026, 8, 1, 14, 10, tzinfo=TZ)
E = 'sensor.bedroom_co2'
def S(state, unit, name): return {'state': state, 'attributes': {'unit_of_measurement': unit, 'friendly_name': name}, 'last_updated': NOW - dt.timedelta(minutes=2)}
STATES = {E: S('1240', 'ppm', 'Bedroom CO2'), 'sensor.bedroom_temp': S('21.4', '°C', 'Bedroom temperature'), 'sensor.bedroom_hum': S('48', '%', 'Bedroom humidity'),
          'sensor.house_energy': S('123456', 'kWh', 'House energy')}
DEVICE_NAMES = {E: 'Bedroom CO2', 'sensor.bedroom_temp': 'Bedroom temperature', 'sensor.bedroom_hum': 'Bedroom humidity', 'sensor.house_energy': 'House energy'}
INPUTS = {'entity': E, 'displays': ['dev1'], 'weekday_format': 'nl'}
