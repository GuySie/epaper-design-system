exec(open(__import__('os').environ['EP_ROOT'] + '/scen/tonight.py').read())
STATES['weather.home']['state'] = 'lightning-rainy'
