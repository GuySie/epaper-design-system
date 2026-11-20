# Claude usage with four bars: the session bar has no resets_at of its own and reads its reset sensor instead
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/claude35.py').read())
del STATES['sensor.s']['attributes']['resets_at']
STATES['sensor.s_reset'] = {'state': '2026-08-01T22:00:00+01:00', 'attributes': {}}
STATES['sensor.x'] = {'state': '12', 'attributes': {'friendly_name': 'Claude Usage (Sam - Max) Extra Usage', 'resets_at': '2026-08-31T00:00:00+01:00'}}
INPUTS.update({'bar_1_reset': 'sensor.s_reset', 'bar_4_period_hours': 720, 'time_format': '12h'})   # the 12-hour reset captions, the widest
