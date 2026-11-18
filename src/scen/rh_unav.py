exec(open(__import__('os').environ['EP_ROOT'] + '/scen/rh.py').read())
# the chosen weather entity is unavailable: another working weather entity serves the forecast
STATES['weather.other'] = dict(STATES['weather.home'])
STATES['weather.home'] = {'state': 'unavailable', 'attributes': {}, 'last_updated': NOW - dt.timedelta(minutes=5)}
FORECASTS = {'weather.other': FORECASTS['weather.home']}
