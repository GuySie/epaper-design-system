# the moon position sensors are unavailable: the sun's timeline without the moon marker
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/sun35.py').read())
STATES['sensor.moon_az']['state'] = 'unavailable'
STATES['sensor.moon_alt']['state'] = 'unavailable'
