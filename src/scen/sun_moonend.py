# night, sun and moon at the right end of the track: the moon has no room on its own side
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/sun_night.py').read())
STATES['sun.sun']['attributes']['azimuth'] = 352
STATES['sensor.moon_az'] = {'state': '354'}
