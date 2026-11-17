import datetime as dt
TZ = dt.timezone(dt.timedelta(hours=1))
NOW = dt.datetime(2026, 8, 1, 14, 10, tzinfo=TZ)
ACCENT = 'red'
cond = ['rainy', 'cloudy', 'cloudy', 'clear-night', 'partlycloudy', 'clear-night', 'clear-night', 'cloudy']
temps = [12, 11, 10, 9, 9, 8, 8, 7]
mm = [1.8, 0.6, 0.2, 0, 0, 0, 0, 0]
hourly = [{'datetime': (NOW.replace(minute=0) + dt.timedelta(hours=i)).isoformat(), 'condition': cond[i], 'temperature': temps[i], 'precipitation': mm[i], 'wind_bearing': 225, 'wind_speed': 15, 'humidity': 80, 'precipitation_probability': 60} for i in range(8)]
dcond = ['partlycloudy', 'rainy', 'pouring', 'cloudy', 'sunny', 'sunny']
daily = [{'datetime': (NOW.replace(hour=12, minute=0) + dt.timedelta(days=i)).isoformat(), 'condition': dcond[i], 'temperature': [13, 11, 10, 12, 14, 15][i],
          'templow': [6, 7, 8, 5, 4, 6][i], 'precipitation': [2.6, 3.2, 12.5, 1.1, 0, 0][i], 'wind_bearing': 225, 'wind_speed': 15, 'humidity': 80, 'precipitation_probability': 60} for i in range(6)]
FORECASTS = {'weather.home': {'hourly': hourly, 'daily': daily}}
STATES = {
 'weather.home': {'state': 'rainy', 'attributes': {'temperature': 12.2, 'temperature_unit': '°C', 'humidity': 81, 'pressure': 1012, 'dew_point': 9,
   'wind_speed': 18, 'wind_bearing': 225, 'wind_speed_unit': 'km/h', 'supported_features': 3}, 'last_updated': NOW - dt.timedelta(minutes=5)},
 'sun.sun': {'state': 'above_horizon', 'attributes': {'next_rising': '2026-08-02T04:51:00+00:00', 'next_setting': '2026-08-01T20:04:00+00:00'}},
 'sensor.moon_phase': {'state': 'waxing_crescent', 'integration': 'moon'},
 'sensor.kleenex_trees': {'state': '96', 'attributes': {'unit_of_measurement': 'ppm', 'details': [{'name': 'Birch', 'value': 96}, {'name': 'Alder', 'value': 12}], 'forecast': [{'value': 40}, {'value': 20}, {'value': 10}, {'value': 5}]}},
}
INPUTS = {'weekday_format': 'nl', 'weather_entity': 'weather.home', 'pollen_sensor': 'sensor.kleenex_trees', 'pollen_type': 'Birch', 'severe_pollen_high': 150, 'location_string': 'Amsterdam'}
