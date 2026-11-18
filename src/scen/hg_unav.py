# the sensor is unavailable now: the line ends at the last reading
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/hg.py').read())
STATES[E]['state'] = 'unavailable'
