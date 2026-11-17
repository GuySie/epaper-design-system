exec(open(__import__('os').environ['EP_ROOT'] + '/scen/entities35.py').read())
import datetime as dt
for e in STATES: STATES[e]['last_reported'] = NOW - dt.timedelta(hours=3)
INPUTS['stale_after'] = 60
INPUTS['header_title'] = 'Living room air quality and energy overview'
