import datetime as dt
TZ = dt.timezone(dt.timedelta(hours=1))
NOW = dt.datetime(2026, 8, 1, 10, 20, tzinfo=TZ)
SIZE = (384, 184)
STATES = {'calendar.work': {'state': 'on', 'attributes': {}}}
def ev(s, e, t): return {'start': s, 'end': e, 'summary': t}
CALENDAR_RESPONSE = {'calendar.work': {'events': [
    ev('2026-08-01T10:00:00+01:00', '2026-08-01T11:30:00+01:00', 'Q4 planning with the whole team and all the partners'),
    ev('2026-08-01T11:45:00+01:00', '2026-08-01T12:15:00+01:00', '1:1 with Theo 🎉'),
    ev('2026-08-01', '2026-08-02', 'All day'),
]}}
INPUTS = {'calendar_entities': ['calendar.work'], 'weekday_format': 'nl'}
