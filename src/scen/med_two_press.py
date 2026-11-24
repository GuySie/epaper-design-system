# a press of the second button (*Medication*, *Several panels, one log*): the hero is its press, the newest, though the first
# button reports an older one; only the pressed button's device flashes (*Blueprint mechanics*, *Button feedback (LED flash)*)
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/med29.py').read())
INPUTS['weekday_format'] = 'en'
INPUTS['time_format'] = '24h'
INPUTS['displays'] = ['dev1', 'dev2']
INPUTS['button_entity'] = ['event.x', 'event.y']
STATES['event.x'] = {'state': (NOW - dt.timedelta(hours=3)).isoformat(), 'attributes': {'event_type': 'button_up'}, 'device_id': 'dev1'}
STATES['event.y'] = {'state': NOW.isoformat(), 'attributes': {'event_type': 'button_up'}, 'device_id': 'dev2'}
MODELS = {'dev1': '2.7" BWRY', 'dev2': '2.7" BWRY'}
TRIGGER = {'platform': 'state', 'id': 'press', 'entity_id': 'event.y', 'to_state': ts}
EXPECT = ['08:14']
EXPECT_FLASH = ['dev2']
