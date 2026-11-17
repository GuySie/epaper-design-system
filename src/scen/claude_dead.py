exec(open(__import__('os').environ['EP_ROOT'] + '/scen/claude35.py').read())
for k in STATES:
    STATES[k]['last_updated'] = NOW - dt.timedelta(hours=7)
    STATES[k]['last_reported'] = NOW - dt.timedelta(hours=2)
