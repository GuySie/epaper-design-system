# one opening's sensor is unavailable
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/openings_1.py').read())
STATES['binary_sensor.kitchen_window']['state'] = 'unavailable'
