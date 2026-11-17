# the widest pollen row the column is made for (a long type, a 3-digit count, severe) together with an alert row: both take a detail row's place
STATES['sensor.wl'] = {'state': 'orange', 'attributes': {}}
STATES['sensor.wt'] = {'state': 'Thunderstorm', 'attributes': {'alerts': [{'title': 'Thunderstorm', 'level': 'orange'}]}}
INPUTS.update({'weather_warning_sensor': 'sensor.wl', 'weather_warning_text_sensor': 'sensor.wt', 'pollen_type': 'Grasses'})
STATES['sensor.kleenex_trees']['state'] = '999'
STATES['sensor.kleenex_trees']['attributes']['details'] = [{'name': 'Grasses', 'value': 999}]
