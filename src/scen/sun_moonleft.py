# night, the moon just left of the sun below the horizon
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/sun_night.py').read())
STATES['sensor.moon_az'] = {'state': '326'}
