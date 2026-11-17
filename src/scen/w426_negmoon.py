exec(open(__import__('os').environ['EP_ROOT'] + '/scen/w426neg.py').read())
STATES['sensor.moon_phase']={'state':'full_moon','attributes':{},'integration':'moon'}
