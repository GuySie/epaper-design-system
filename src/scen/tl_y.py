# a panel with red and yellow
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/tl.py').read())
INPUTS['displays'] = ['dev1']
MODELS = {'dev1': 'BWRY'}
