exec(open(__import__('os').environ['EP_ROOT'] + '/scen/wx.py').read())
STATES['sensor.wl'] = {'state': 'orange', 'attributes': {}}
STATES['sensor.wt'] = {'state': 'Thunderstorm', 'attributes': {'alerts': [{'title': 'Thunderstorm', 'level': 'orange'}]}}
INPUTS.update({'weather_warning_sensor': 'sensor.wl', 'weather_warning_text_sensor': 'sensor.wt'})

INPUTS['displays'] = ['d1']
MODELS = {'d1': 'X BWRY'}
