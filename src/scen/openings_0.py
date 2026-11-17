exec(open(__import__('os').environ['EP_ROOT'] + '/scen/openings_1.py').read())
for e in STATES: STATES[e]['state']='off'
