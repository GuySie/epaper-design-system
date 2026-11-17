# the widest chip in 12-hour form: Croatian, missed (PROPUŠTENO), the widest short weekday and month (PO, VEL), a wide day number (24), AM
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/med29.py').read())
NOW = dt.datetime(2026, 2, 25, 22, 30, tzinfo=TZ)
INPUTS['button_entity'] = 'event.x'
INPUTS['time_format'] = '12h'
INPUTS['weekday_format'] = 'hr'
STATES['event.x'] = {'state': dt.datetime(2026, 2, 23, 10, 44, tzinfo=TZ).isoformat(), 'attributes': {'event_type': 'button_up'}}
MODELS = {'dev1': '2.7" BWRY'}
