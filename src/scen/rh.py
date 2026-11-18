# Rain forecast: a weather entity's hourly forecast, a heavy shower in the evening (severe) and a little more at night
import datetime as dt
TZ = dt.timezone(dt.timedelta(hours=1))
NOW = dt.datetime(2026, 8, 1, 14, 7, 30, tzinfo=TZ)
MM = [0, 0, 0.2, 0.6, 1.4, 3.1, 6.5, 12.0, 4.2, 1.1, 0.3, 0, 0, 0, 0, 0.4, 0.9, 0.5, 0, 0, 0, 0, 0, 0]


def hourly(mm, now):
    """48 hours from the current hour; past the hours given, dry"""
    t0 = now.replace(minute=0, second=0, microsecond=0)
    return [{'datetime': (t0 + dt.timedelta(hours=i)).isoformat(), 'condition': 'rainy' if (mm[i] if i < len(mm) else 0) > 0 else 'cloudy',
             'temperature': 12, 'precipitation': mm[i] if i < len(mm) else 0, 'wind_bearing': 225, 'wind_speed': 15} for i in range(48)]


FORECASTS = {'weather.home': {'hourly': hourly(MM, NOW), 'daily': []}}
STATES = {'weather.home': {'state': 'rainy', 'attributes': {'temperature': 12.2, 'temperature_unit': '°C', 'precipitation_unit': 'mm', 'supported_features': 3},
                           'last_updated': NOW - dt.timedelta(minutes=5)}}
INPUTS = {'weekday_format': 'nl', 'weather_entity': 'weather.home'}
