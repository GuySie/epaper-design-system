import datetime as dt
TZ = dt.timezone(dt.timedelta(hours=1))
NOW = dt.datetime(2026, 8, 3, 20, 30, tzinfo=TZ)
ACCENT = 'red'
cond = ['fog', 'fog', 'fog', 'fog', 'fog', 'clear-night', 'clear-night', 'clear-night']
temps = [4, 4, 4, 3, 3, 2, 2, 2]
mm = [0] * 8
hourly = [{'datetime': (NOW.replace(minute=0) + dt.timedelta(hours=i)).isoformat(), 'condition': cond[i], 'temperature': temps[i], 'precipitation': mm[i], 'wind_bearing': 100, 'wind_speed': 2, 'humidity': 98, 'precipitation_probability': 10} for i in range(8)]
dcond = ['clear-night', 'partlycloudy', 'pouring', 'partlycloudy', 'partlycloudy', 'partlycloudy']
daily = [{'datetime': (NOW.replace(hour=12, minute=0) + dt.timedelta(days=i)).isoformat(), 'condition': dcond[i], 'temperature': [11, 9, 6, 9, 9, 9][i],
          'templow': [3, 2, 2, 3, 4, 2][i], 'precipitation': [0, 1, 16, 0, 1, 0][i], 'wind_bearing': 100, 'wind_speed': 11, 'humidity': 90, 'precipitation_probability': 30} for i in range(6)]
FORECASTS = {'weather.home': {'hourly': hourly, 'daily': daily}}
STATES = {
 'weather.home': {'state': 'fog', 'attributes': {'temperature': 7, 'temperature_unit': '°C', 'humidity': 98, 'pressure': 1016, 'dew_point': 2.5,
   'wind_speed': 2, 'wind_bearing': 100, 'wind_speed_unit': 'km/h', 'precipitation_unit': 'mm', 'pressure_unit': 'hPa', 'supported_features': 3}, 'last_updated': NOW - dt.timedelta(minutes=5)},
 'sun.sun': {'state': 'below_horizon', 'attributes': {'next_rising': '2026-08-04T06:50:00+00:00', 'next_setting': '2026-08-04T15:55:00+00:00'}},
 'sensor.moon_phase': {'state': 'waning_crescent', 'integration': 'moon'},
 'sensor.kleenex_trees': {'state': '0', 'attributes': {'unit_of_measurement': 'ppm', 'details': [{'name': 'Birch', 'value': 0}], 'forecast': [{'value': 0}]}},
}
INPUTS = {'weekday_format': 'nl', 'weather_entity': 'weather.home', 'pollen_sensor': 'sensor.kleenex_trees', 'pollen_type': 'Birch', 'displays': ['d1']}
MODELS = {'d1': 'X BWRY'}
