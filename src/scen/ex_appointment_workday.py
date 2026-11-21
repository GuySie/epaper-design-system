# an example of what the page is used for (README, lib/pictures.py): in English, on a BWRY panel
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/appt35.py').read())
TZ = dt.timezone(dt.timedelta(hours=1))
NOW = dt.datetime(2026, 8, 3, 9, 40, tzinfo=TZ)
STATES = {'calendar.work': {'state': 'on', 'attributes': {}}}
def ev(s, e, t): return {'start': s, 'end': e, 'summary': t}
CALENDAR_RESPONSE = {'calendar.work': {'events': [
    ev('2026-08-03T09:30:00+01:00', '2026-08-03T09:45:00+01:00', 'Stand-up'),
    ev('2026-08-03T10:00:00+01:00', '2026-08-03T11:00:00+01:00', 'Design review'),
    ev('2026-08-03T12:30:00+01:00', '2026-08-03T13:30:00+01:00', 'Lunch with Sam'),
    ev('2026-08-03T16:00:00+01:00', '2026-08-03T16:30:00+01:00', 'Client call'),
]}}
INPUTS = {'calendar_entities': ['calendar.work'], 'weekday_format': 'en', 'displays': ['dev1']}
MODELS = {'dev1': 'BWRY'}
