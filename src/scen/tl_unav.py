# one entity unavailable
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/tl.py').read())
STATES['sensor.living']['state'] = 'unavailable'
