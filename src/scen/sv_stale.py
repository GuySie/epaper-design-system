# the sensor stopped reporting 3 hours ago
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/sv.py').read())
STATES[E]['last_reported'] = NOW - dt.timedelta(hours=3)
STATES[E]['last_updated'] = NOW - dt.timedelta(hours=3)
INPUTS['stale_after'] = 60
