import datetime as dt
TZ = dt.timezone(dt.timedelta(hours=1))
NOW = dt.datetime(2026, 8, 1, 10, 20, tzinfo=TZ)
STATES = {'calendar.home': {'state': 'on', 'attributes': {}}}
def ev(d, s, e, t): return {'start': f'2026-08-0{d}T{s}:00+01:00', 'end': f'2026-08-0{d}T{e}:00+01:00', 'summary': t}
CALENDAR_RESPONSE = {'calendar.home': {'events': [
    ev(1, '10:00', '11:30', 'Quarter planning'), ev(1, '14:00', '15:00', 'Dentist'), ev(1, '19:30', '22:00', 'Birthday party for Nina and Ruben'),
    ev(2, '11:00', '15:00', 'Family visit'), ev(3, '09:00', '10:00', 'Running'), ev(3, '13:00', '14:00', 'Team meeting'),
    ev(3, '15:30', '16:30', 'Sprint review'), ev(4, '08:30', '09:30', 'Garage'), ev(4, '12:00', '13:00', 'Lunch with Sam'), ev(6, '10:00', '11:00', 'Haircut'),
    {'start': '2026-08-02', 'end': '2026-08-03', 'summary': 'Street fair'},
]}}
INPUTS = {'calendar_entities': ['calendar.home'], 'weekday_format': 'nl'}
