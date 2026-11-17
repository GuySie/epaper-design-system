exec(open(__import__('os').environ['EP_ROOT'] + '/scen/w426.py').read())
# the error view: the weather entity is unavailable
STATES['weather.home'] = {'state': 'unavailable', 'attributes': {}}
