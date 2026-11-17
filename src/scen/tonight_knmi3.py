exec(open(__import__('os').environ['EP_ROOT'] + '/scen/tonight.py').read())
STATES['sensor.wl'] = {'state': 'orange', 'attributes': {}}
STATES['sensor.wt'] = {'state': 'none', 'attributes': {'alerts': [{'code': 'orange', 'headline': 'Severe gusts and thunderstorms'}]}}
INPUTS.update({'weather_warning_sensor': 'sensor.wl', 'weather_warning_text_sensor': 'sensor.wt'})
