import datetime as dt
TZ = dt.timezone(dt.timedelta(hours=1))
NOW = dt.datetime(2026, 8, 2, 21, 54, tzinfo=TZ)
SIZE = (384, 184)
STATES = {'calendar.work': {'state': 'on', 'attributes': {}}}
def ev(s, e, t): return {'start': s, 'end': e, 'summary': t}
CALENDAR_RESPONSE = {'calendar.work': {'events': [
    ev('2026-08-03T09:00:00+01:00', '2026-08-03T10:30:00+01:00', 'Heron weekly plan'),
    ev('2026-08-03T10:30:00+01:00', '2026-08-03T12:00:00+01:00', 'Heron team review prep'),
    ev('2026-08-03T14:00:00+01:00', '2026-08-03T15:00:00+01:00', 'Kestrel research weekly'),
    ev('2026-08-03T15:00:00+01:00', '2026-08-03T15:30:00+01:00', 'Osprey go-live'),
]}}
INPUTS = {'calendar_entities': ['calendar.work'], 'weekday_format': 'nl'}
