# Plant moisture whose sensors stopped reporting 3 hours ago
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/plants42.py').read())
for e in STATES:
    STATES[e]['last_reported'] = NOW - dt.timedelta(hours=3)
    STATES[e]['last_updated'] = NOW - dt.timedelta(hours=3)
INPUTS['stale_after'] = 60
