# low, at severe: humidity at or below 20 %
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/sv.py').read())
STATES['sensor.bedroom_hum']['state'] = '18'
INPUTS.update({'entity': 'sensor.bedroom_hum', 'flag_low': True, 'warning_low': 30, 'severe_low': 20})
