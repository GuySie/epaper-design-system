# the button's event entity is unavailable (the device is offline)
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/med29.py').read())
INPUTS['button_entity'] = 'event.x'
STATES['event.x'] = {'state': 'unavailable', 'attributes': {}}
MODELS = {'dev1': '2.7" BWRY'}
