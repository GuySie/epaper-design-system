# another configuration: a reading longer than the layouts are fitted for steps down the hero ladder (123456 kWh)
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/sv.py').read())
INPUTS['entity'] = 'sensor.house_energy'
