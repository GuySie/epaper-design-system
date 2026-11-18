# the widest reading the layouts are fitted for: four characters and a three-letter unit (-12.5 °C)
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/sv.py').read())
STATES['sensor.bedroom_temp']['state'] = '-12.5'
INPUTS['entity'] = 'sensor.bedroom_temp'
