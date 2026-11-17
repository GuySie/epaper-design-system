exec(open(__import__('os').environ['EP_ROOT'] + '/scen/sun35.py').read())
STATES['zone.home'] = {'state': '0', 'attributes': {'latitude': -33.9, 'longitude': 151.2}}
STATES['sun.sun']['attributes']['azimuth'] = 20; STATES['sun.sun']['attributes']['elevation'] = 70
INPUTS['hemisphere'] = 'southern'; INPUTS['weekday_format'] = 'en'
