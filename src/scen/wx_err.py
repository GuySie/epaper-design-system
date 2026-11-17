exec(open(__import__('os').environ['EP_ROOT'] + '/scen/wx.py').read())
STATES['weather.home'] = {'state': 'unavailable', 'attributes': {}}
INPUTS['displays'] = ['d1']
MODELS = {'d1': 'X BWRY'}
