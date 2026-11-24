exec(open(__import__('os').environ['EP_ROOT'] + '/scen/med29.py').read())
INPUTS['button_entity'] = 'event.x'
STATES['event.x'] = {'state': (NOW - dt.timedelta(hours=40)).isoformat(), 'attributes': {'event_type': 'button_up'}}
MODELS = {'dev1': '2.7" BWRY'}
EXPECT_FIRES = ['overdue']   # the deadline trigger fires (*Medication*, *Medication redraws by itself*)
