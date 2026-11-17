exec(open(__import__('os').environ['EP_ROOT'] + '/scen/wx.py').read())
STATES['sensor.kleenex_trees']['state'] = '0'
STATES['sensor.kleenex_trees']['attributes']['details'] = [{'name': 'Birch', 'value': 0}]
