exec(open(__import__('os').environ['EP_ROOT'] + '/scen/wxp16.py').read())
STATES['sensor.wl'] = {'state': 'yellow', 'attributes': {}}
INPUTS.update({'weather_warning_sensor': 'sensor.wl'})
MODELS = {k: '1.4" BWRY' for k in ['dev1','e1','d1']}

INPUTS['displays'] = ['d1']
MODELS = {'d1': 'X BWRY'}
