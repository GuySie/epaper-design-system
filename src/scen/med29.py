import datetime as dt
TZ = dt.timezone(dt.timedelta(hours=1))
NOW = dt.datetime(2026, 8, 1, 8, 14, tzinfo=TZ)
STATES = {}
class O: pass
ts = O(); ts.attributes = {'event_type': 'button_up'}
TRIGGER = {'to_state': ts}
INPUTS = {'weekday_format': 'nl', 'displays': 'dev1'}
# the normal case: the button was pressed just now (the other cases set their own press)
INPUTS['button_entity'] = 'event.x'
STATES['event.x'] = {'state': NOW.isoformat(), 'attributes': {'event_type': 'button_up'}}
