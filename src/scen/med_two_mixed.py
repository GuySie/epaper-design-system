# a BWRY and a black/white panel (the colour one first), missed (*Medication*, *Several panels, one log*; *Values per panel*, *Not configurable*):
# both draw what every selected panel has, black and white
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/med29.py').read())
INPUTS['weekday_format'] = 'en'
INPUTS['time_format'] = '24h'
INPUTS['displays'] = ['dev1', 'dev2']
INPUTS['button_entity'] = ['event.x', 'event.y']
STATES['event.x'] = {'state': (NOW - dt.timedelta(hours=50)).isoformat(), 'attributes': {'event_type': 'button_up'}}
STATES['event.y'] = {'state': (NOW - dt.timedelta(hours=40)).isoformat(), 'attributes': {'event_type': 'button_up'}}
MODELS = {'dev1': '2.7" BWRY', 'dev2': '2.7" BW'}
EXPECT = ['MISSED']
EXPECT_COLOURS = ['black', 'white']
