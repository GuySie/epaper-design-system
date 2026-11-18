# the sensor is unavailable
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/sv.py').read())
STATES[E]['state'] = 'unavailable'
