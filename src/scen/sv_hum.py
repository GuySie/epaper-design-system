# another configuration: a short reading with an icon (48 %)
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/sv.py').read())
INPUTS.update({'entity': 'sensor.bedroom_hum', 'icon': 'mdi:water-percent'})
