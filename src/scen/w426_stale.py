exec(open(__import__('os').environ['EP_ROOT'] + '/scen/w426.py').read())
# stale: the weather entity last reported 5 hours ago
import datetime as _dt
STATES['weather.home']['last_updated'] = NOW - _dt.timedelta(hours=5)
INPUTS['stale_after'] = 60
