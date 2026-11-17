exec(open(__import__('os').environ['EP_ROOT'] + '/scen/wxp16.py').read())
STATES['weather.home']['attributes']['temperature'] = 10.0
