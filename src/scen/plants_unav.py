exec(open(__import__('os').environ['EP_ROOT'] + '/scen/plants8.py').read())
# most plant sensors unavailable: the error state
for i in range(5):
    STATES[f'sensor.p{i}']['state'] = 'unavailable'
