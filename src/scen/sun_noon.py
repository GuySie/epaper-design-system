exec(open(__import__('os').environ['EP_ROOT'] + '/scen/sun35.py').read())
NOW = dt.datetime(2026, 2, 1, 12, 28, tzinfo=TZ)
STATES['sun.sun']['attributes']['azimuth'] = 180; STATES['sun.sun']['attributes']['elevation'] = 19.5
STATES['sensor.moon_az'] = {'state': '250'}; STATES['sensor.moon_alt'] = {'state': '-20'}
