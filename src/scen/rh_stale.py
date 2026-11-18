exec(open(__import__('os').environ['EP_ROOT'] + '/scen/rh.py').read())
# the weather entity stopped reporting
STATES['weather.home']['last_updated'] = NOW - dt.timedelta(minutes=95)
