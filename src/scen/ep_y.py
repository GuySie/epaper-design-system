exec(open(__import__('os').environ['EP_ROOT'] + '/scen/ep.py').read())
INPUTS['displays'] = ['dev1']
MODELS = {'dev1': 'BWRY'}
