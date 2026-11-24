# two buttons, neither reports a press (one unavailable, one unknown): no redraw, the panels keep the last press
# (*Medication*, *No press, no redraw*)
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/med29.py').read())
INPUTS['displays'] = ['dev1', 'dev2']
INPUTS['button_entity'] = ['event.x', 'event.y']
STATES['event.x'] = {'state': 'unavailable', 'attributes': {}}
STATES['event.y'] = {'state': 'unknown', 'attributes': {}}
MODELS = {'dev1': '2.7" BWRY', 'dev2': '2.7" BWRY'}
EXPECT_NO_DRAW = True
