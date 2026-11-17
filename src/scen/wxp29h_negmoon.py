exec(open(__import__('os').environ['EP_ROOT'] + '/scen/wxp29h_neg.py').read())
STATES['sensor.moon_phase']={'state':'full_moon','attributes':{},'integration':'moon'}
