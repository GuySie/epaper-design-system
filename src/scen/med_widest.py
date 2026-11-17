# the widest reading (registry: 20:00): the widest hero time, pressed yesterday evening, still on time
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/med29.py').read())
INPUTS['button_entity'] = 'event.x'
INPUTS['time_format'] = '24h'
STATES['event.x'] = {'state': (NOW.replace(hour=20, minute=0) - dt.timedelta(days=1)).isoformat(), 'attributes': {'event_type': 'button_up'}}
