exec(open(__import__('os').environ['EP_ROOT'] + '/scen/rh.py').read())
# the error view: the weather entity has no hourly forecast (daily only)
STATES['weather.home']['attributes']['supported_features'] = 1
