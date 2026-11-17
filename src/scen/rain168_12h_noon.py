# 12-hour time across noon on the 2.7", the widest footer
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/rain168.py').read())
NOW = dt.datetime(2026, 8, 1, 11, 7, 30, tzinfo=TZ)
start = (int(NOW.timestamp()) // 300) * 300
STATES['sensor.neerslag_buienalarm_regen_data']['attributes']['data']['start'] = start
for k in STATES: STATES[k]['last_updated'] = NOW - dt.timedelta(minutes=3)
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/_rain_widest.py').read())
INPUTS['time_format'] = '12h'
