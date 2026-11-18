# another configuration: an icon beside the number and a second value under it
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/sv.py').read())
INPUTS.update({'entity': 'sensor.bedroom_temp', 'secondary_entity': 'sensor.bedroom_hum', 'icon': 'mdi:thermometer'})
