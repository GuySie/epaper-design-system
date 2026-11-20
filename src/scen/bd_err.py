# the error view: no bin has a date to come
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/bd.py').read())
for k in STATES: STATES[k]['state'] = 'unknown'
