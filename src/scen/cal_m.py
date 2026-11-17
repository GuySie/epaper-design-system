import datetime as dt
TZ = dt.timezone(dt.timedelta(hours=1))
NOW = dt.datetime(2026, 8, 2, 21, 35, tzinfo=TZ)
STATES = {'calendar.work': {'state': 'on', 'attributes': {}}}
def ev(d, s, e, t): return {'start': f'2026-08-{d - 6:02d}T{s}:00+01:00', 'end': f'2026-08-{d - 6:02d}T{e}:00+01:00', 'summary': t}
CALENDAR_RESPONSE = {'calendar.work': {'events': [
    ev(9,'09:00','10:30','Heron weekly plan'), ev(9,'10:30','12:00','Heron team review prep'), ev(9,'14:00','15:00','Kestrel research weekly'),
    ev(9,'15:00','15:30','Osprey go-live'), ev(9,'16:30','17:30','Lantern design weekly'),
    ev(10,'09:30','10:00','Standup'), ev(10,'11:00','12:00','Vendor call'), ev(10,'14:00','15:00','Logo critique'), ev(10,'16:00','16:30','1:1 Jasper'),
    ev(11,'10:00','11:00','Patent catchup'), ev(11,'13:00','14:00','Newsletter planning'),
    ev(12,'09:00','17:00','Offsite'), ev(13,'10:00','11:00','Retro'),
]}}
INPUTS = {'calendar_entities': ['calendar.work'], 'weekday_format': 'nl'}
