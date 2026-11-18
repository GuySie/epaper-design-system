# every entity unavailable: the error state (on a screen with one tile: a dash)
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/tl.py').read())
for e in STATES:
    STATES[e]['state'] = 'unavailable'
