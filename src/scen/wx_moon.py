exec(open(__import__('os').environ['EP_ROOT'] + '/scen/wx.py').read())
STATES['sensor.moon_phase']={'state':'waxing_crescent','attributes':{},'integration':'moon'}
