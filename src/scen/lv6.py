# six rows (the 4.1")
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/lv.py').read())
INPUTS.update({'bar_5': 'sensor.disk', 'bar_6': 'sensor.co2', 'bar_6_max': 2000})
