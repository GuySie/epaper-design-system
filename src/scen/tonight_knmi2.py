exec(open(__import__('os').environ['EP_ROOT'] + '/scen/tonight.py').read())
STATES['sensor.wl'] = {'state': 'yellow', 'attributes': {}}
STATES['sensor.wt'] = {'state': 'none', 'attributes': {'alert_count': 1, 'alerts': [{'code': 'yellow', 'condition': 'fog', 'description': 'Fog in more and more places, with visibility under 200 m.', 'headline': 'Dense fog in places'}]}}
INPUTS.update({'weather_warning_sensor': 'sensor.wl', 'weather_warning_text_sensor': 'sensor.wt'})
