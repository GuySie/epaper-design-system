# one row unavailable
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/lv.py').read())
STATES['sensor.tank']['state'] = 'unavailable'
