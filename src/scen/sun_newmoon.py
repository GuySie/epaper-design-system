exec(open(__import__('os').environ['EP_ROOT'] + '/scen/sun35.py').read())
STATES['sensor.moon_phase'] = {'state': 'new_moon', 'attributes': {}, 'integration': 'moon'}
STATES['sensor.moon_az'] = {'state': '214'}; STATES['sensor.moon_alt'] = {'state': '16'}
