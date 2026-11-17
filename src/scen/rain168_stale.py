exec(open(__import__('os').environ['EP_ROOT'] + '/scen/rain168.py').read())
# stale: the rain sources last reported 95 minutes ago
for k in STATES: STATES[k]['last_updated'] = NOW - dt.timedelta(minutes=95)
