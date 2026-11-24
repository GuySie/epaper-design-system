# the button with the newest press goes offline (*Medication*, *Several panels, one log*): it is left out, so the older press
# counts and its deadline redraws the panels; the redraw that a deadline starts flashes no LED, though its trigger carries the
# button that changed (*Medication*, *Medication redraws by itself*)
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/med29.py').read())
INPUTS['weekday_format'] = 'en'
INPUTS['time_format'] = '24h'
INPUTS['displays'] = ['dev1', 'dev2']
INPUTS['button_entity'] = ['event.x', 'event.y']
STATES['event.x'] = {'state': 'unavailable', 'attributes': {}, 'device_id': 'dev1'}
STATES['event.y'] = {'state': (NOW - dt.timedelta(hours=40)).isoformat(), 'attributes': {'event_type': 'button_up'}, 'device_id': 'dev2'}
MODELS = {'dev1': '2.7" BWRY', 'dev2': '2.7" BWRY'}
TRIGGER = {'platform': 'template', 'id': 'overdue', 'entity_id': 'event.x', 'to_state': ts}
EXPECT = ['MISSED']
EXPECT_FIRES = ['overdue']
EXPECT_FLASH = []
