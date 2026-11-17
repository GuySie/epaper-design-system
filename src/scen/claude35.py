import datetime as dt
TZ = dt.timezone(dt.timedelta(hours=1))
NOW = dt.datetime(2026, 8, 1, 20, 45, tzinfo=TZ)
SIZE = (384, 184)
STATES = {
 'sensor.s': {'state': '38', 'attributes': {'friendly_name': 'Claude Usage (Sam - Max) Session Usage', 'resets_at': '2026-08-01T22:00:00+01:00'}, 'last_updated': NOW - dt.timedelta(minutes=2)},
 'sensor.w': {'state': '92', 'attributes': {'friendly_name': 'Claude Usage (Sam - Max) Week Usage', 'resets_at': '2026-08-03T09:00:00+01:00'}},
 'sensor.o': {'state': '47', 'attributes': {'friendly_name': 'Claude Usage (Sam - Max) Weekly Sonnet Usage', 'resets_at': '2026-08-03T09:00:00+01:00'}},
 'sensor.x': {'state': 'unavailable', 'attributes': {'friendly_name': 'Claude Usage (Sam - Max) Extra Usage'}},
}
INPUTS = {'bar_1': 'sensor.s', 'bar_1_period_hours': 5, 'bar_2': 'sensor.w', 'bar_2_period_hours': 168,
          'bar_3': 'sensor.o', 'bar_3_period_hours': 168, 'bar_4': 'sensor.x', 'weekday_format': 'nl'}
