# the first bin's sensor is unavailable, another's date has passed: the next one is shown
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/bd.py').read())
STATES['sensor.bin_paper']['state'] = 'unavailable'
STATES['sensor.bin_plastic']['state'] = D(-2)
