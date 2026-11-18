# the sensor and one detail unavailable
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/vd.py').read())
STATES[E]['state'] = 'unavailable'
STATES['sensor.h']['state'] = 'unavailable'
