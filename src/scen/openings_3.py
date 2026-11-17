exec(open(__import__('os').environ['EP_ROOT'] + '/scen/openings_1.py').read())
for e in ['binary_sensor.hallway_front_door','binary_sensor.kitchen_window']: STATES[e]['state']='on'
