import datetime as dt
TZ = dt.timezone(dt.timedelta(hours=1))
NOW = dt.datetime(2026, 8, 1, 8, 14, tzinfo=TZ)
SIZE = (384, 168)
STATES = {}
class O: pass
ts = O(); ts.attributes = {'event_type': 'button_up'}
TRIGGER = {'to_state': ts}
INPUTS = {'weekday_format': 'nl', 'displays': 'dev1'}
