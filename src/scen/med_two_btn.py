# two panels, two buttons (*Medication*, *Several panels, one log*): the newest press is the hero and the deadlines count from it;
# the newer press is the first button's, the older one (past the severe time) the last's
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/med29.py').read())
INPUTS['weekday_format'] = 'en'
INPUTS['time_format'] = '24h'
INPUTS['displays'] = ['dev1', 'dev2']
INPUTS['button_entity'] = ['event.x', 'event.y']
STATES['event.x'] = {'state': (NOW - dt.timedelta(hours=2)).isoformat(), 'attributes': {'event_type': 'button_up'}}
STATES['event.y'] = {'state': (NOW - dt.timedelta(hours=40)).isoformat(), 'attributes': {'event_type': 'button_up'}}
MODELS = {'dev1': '2.7" BWRY', 'dev2': '2.7" BWRY'}
EXPECT = ['06:14']
EXPECT_NOT = ['OVERDUE', 'MISSED']
EXPECT_FIRES = []     # neither deadline fires: they count from the newest press
