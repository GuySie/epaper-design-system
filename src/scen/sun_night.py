exec(open(__import__('os').environ['EP_ROOT'] + '/scen/sun35.py').read())
NOW = dt.datetime(2026, 2, 1, 21, 50, tzinfo=TZ)
STATES['sun.sun']['attributes']['elevation'] = -50.7
STATES['sun.sun']['attributes']['azimuth'] = 330
STATES['sensor.moon_az'] = {'state': '331.7'}; STATES['sensor.moon_alt'] = {'state': '-55'}
STATES['sensor.moon_phase'] = {'state': 'new_moon', 'attributes': {}, 'integration': 'moon'}
