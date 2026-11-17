exec(open(__import__('os').environ['EP_ROOT'] + '/scen/rain168.py').read())
# a panel with yellow (BWRY): warning fills
INPUTS['displays'] = ['dev1']
MODELS = {'dev1': 'BWRY'}
