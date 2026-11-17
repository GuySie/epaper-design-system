exec(open(__import__('os').environ['EP_ROOT'] + '/scen/wx75p.py').read())
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/_calendar.py').read())
import datetime as _dt
STATES['weather.home']['last_updated'] = NOW - _dt.timedelta(hours=5)
INPUTS['stale_after'] = 60
