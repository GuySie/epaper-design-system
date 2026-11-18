# the widest reading (1240 ppm) beside a long label
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/lv.py').read())
INPUTS.update({'bar_4': 'sensor.co2', 'bar_4_max': 2000, 'bar_4_label': 'Bedroom carbon dioxide level'})
