# Levels: four sensors with their own maximum (a battery, solar power of 4 kW, a tank of 1000 L, humidity)
import datetime as dt
TZ = dt.timezone(dt.timedelta(hours=1))
NOW = dt.datetime(2026, 8, 1, 14, 10, tzinfo=TZ)
def S(state, unit, name): return {'state': state, 'attributes': {'unit_of_measurement': unit, 'friendly_name': name}, 'last_updated': NOW - dt.timedelta(minutes=2)}
STATES = {'sensor.battery': S('82', '%', 'Home battery'), 'sensor.solar': S('1.8', 'kW', 'Solar power'), 'sensor.tank': S('340', 'L', 'Rain water tank'),
          'sensor.humidity': S('48', '%', 'Living room humidity'), 'sensor.disk': S('91', '%', 'Server disk'), 'sensor.co2': S('1240', 'ppm', 'Bedroom CO2')}
DEVICE_NAMES = {e: d['attributes']['friendly_name'] for e, d in STATES.items()}
INPUTS = {'bar_1': 'sensor.battery', 'bar_2': 'sensor.solar', 'bar_2_max': 4, 'bar_3': 'sensor.tank', 'bar_3_max': 1000, 'bar_4': 'sensor.humidity',
          'displays': ['dev1'], 'weekday_format': 'nl'}
