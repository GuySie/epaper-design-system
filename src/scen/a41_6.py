import datetime as dt
TZ = dt.timezone(dt.timedelta(hours=1))
NOW = dt.datetime(2026, 8, 3, 9, 40, tzinfo=TZ)
SIZE = (400, 300)
STATES = {'calendar.work': {'state': 'on', 'attributes': {}}}
def ev(s, e, t): return {'start': s, 'end': e, 'summary': t}
EV = [
    ev('2026-08-03T09:00:00+01:00', '2026-08-03T10:30:00+01:00', 'Heron weekly plan'),
    ev('2026-08-03T10:30:00+01:00', '2026-08-03T12:00:00+01:00', 'Heron team review prep'),
    ev('2026-08-03T14:00:00+01:00', '2026-08-03T15:00:00+01:00', 'Kestrel research weekly'),
    ev('2026-08-03T15:00:00+01:00', '2026-08-03T15:30:00+01:00', 'Osprey go-live'),
    ev('2026-08-03T16:30:00+01:00', '2026-08-03T17:00:00+01:00', 'Lantern design weekly'),
    ev('2026-08-04T09:30:00+01:00', '2026-08-04T10:00:00+01:00', 'Sam / Anne-Loïse'),
    ev('2026-08-04T11:00:00+01:00', '2026-08-04T12:00:00+01:00', 'Supplier weekly status update'),
]
CALENDAR_RESPONSE = {'calendar.work': {'events': EV}}
INPUTS = {'calendar_entities': ['calendar.work'], 'weekday_format': 'nl', 'displays': ['d1']}
MODELS = {'d1': '4.1" BWRY'}
