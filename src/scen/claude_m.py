exec(open(__import__('os').environ['EP_ROOT'] + '/scen/claude35.py').read())
NOW = dt.datetime(2026, 8, 2, 21, 47, tzinfo=TZ)
STATES = {
 'sensor.s': {'state': '26', 'attributes': {'friendly_name': 'Claude Usage (Sam - Pro) Session Usage', 'resets_at': '2026-08-03T00:20:00+01:00'}},
 'sensor.w': {'state': '20', 'attributes': {'friendly_name': 'Claude Usage (Sam - Pro) Week Usage', 'resets_at': '2026-08-03T20:00:00+01:00'}},
 'sensor.x': {'state': 'unavailable', 'attributes': {'friendly_name': 'Claude Usage (Sam - Pro) Extra Usage'}},
}
INPUTS = {'bar_1': 'sensor.s', 'bar_1_period_hours': 5, 'bar_2': 'sensor.w', 'bar_2_period_hours': 168, 'bar_3': 'sensor.x', 'weekday_format': 'nl', 'header_title': 'Claude usage'}
