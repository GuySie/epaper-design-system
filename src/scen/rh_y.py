exec(open(__import__('os').environ['EP_ROOT'] + '/scen/rh_warn.py').read())
INPUTS['displays'] = ['dev1']
MODELS = {'dev1': 'BWRY'}
