exec(open(__import__('os').environ['EP_ROOT'] + '/scen/wx.py').read())
STATES['sensor.kleenex_trees']['state']='10'
STATES['sensor.kleenex_trees']['attributes']['details'][0]['value']=10
