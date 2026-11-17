exec(open(__import__('os').environ['EP_ROOT'] + '/scen/rain35.py').read())
for k in STATES: STATES[k]['last_updated'] = NOW - dt.timedelta(minutes=95)
INPUTS['time_format'] = '24h'
ACCENT = 'yellow'
INPUTS['accent_color'] = 'yellow'
