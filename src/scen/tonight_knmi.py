exec(open(__import__('os').environ['EP_ROOT'] + '/scen/tonight.py').read())
STATES['sensor.wl'] = {'state': 'yellow', 'attributes': {}}
STATES['sensor.wt'] = {'state': 'Fog', 'attributes': {'alerts': [{'title': 'Fog', 'level': 'yellow'}]}}
INPUTS.update({'weather_warning_sensor': 'sensor.wl', 'weather_warning_text_sensor': 'sensor.wt'})
