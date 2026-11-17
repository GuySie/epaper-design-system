# the reference picture of this layout (lib/pictures.py): its ordinary state, in English, on a BWRY panel
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/openings_1.py').read())
INPUTS['weekday_format'] = 'en'
INPUTS['displays'] = ['dev1']
MODELS = {'dev1': 'BWRY'}
# the page shows one level at a time: the severe one (the front door is open)
STATES['binary_sensor.hallway_front_door']['state'] = 'on'
