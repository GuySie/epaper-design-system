exec(open(__import__('os').environ['EP_ROOT'] + '/scen/wx75neg.py').read())
STATES['sensor.moon_phase']={'state':'full_moon','attributes':{},'integration':'moon'}
