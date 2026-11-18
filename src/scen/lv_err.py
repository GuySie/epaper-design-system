# most rows unavailable: the error state
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/lv.py').read())
for e in ('sensor.tank', 'sensor.solar', 'sensor.battery'):
    STATES[e]['state'] = 'unavailable'
