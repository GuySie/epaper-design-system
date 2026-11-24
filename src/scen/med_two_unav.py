# two buttons, one unavailable (*Medication*, *Several panels, one log*): it is left out, the other's press is the hero;
# the first button is the unavailable one, so an unavailable button read as a press fails
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/med29.py').read())
INPUTS['weekday_format'] = 'en'
INPUTS['time_format'] = '24h'
INPUTS['displays'] = ['dev1', 'dev2']
INPUTS['button_entity'] = ['event.x', 'event.y']
STATES['event.x'] = {'state': 'unavailable', 'attributes': {}}
STATES['event.y'] = {'state': (NOW - dt.timedelta(hours=2)).isoformat(), 'attributes': {'event_type': 'button_up'}}
MODELS = {'dev1': '2.7" BWRY', 'dev2': '2.7" BWRY'}
EXPECT = ['06:14']
