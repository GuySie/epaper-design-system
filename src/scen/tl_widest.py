# the widest readings: a state and labels too long for a tile
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/tl.py').read())
TRANSLATED['binary_sensor.window'] = 'Disconnected'
INPUTS['entity_1_label'] = 'Alarm system upstairs'
INPUTS['entity_2_label'] = 'Front door of the garden house'
STATES['sensor.living']['state'] = '-12.5'
