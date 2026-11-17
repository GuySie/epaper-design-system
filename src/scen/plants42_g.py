exec(open(__import__('os').environ['EP_ROOT'] + '/scen/plants42.py').read())
INPUTS['displays'] = ['g1']
MODELS = {'g1': '7.5" GRAYSCALE_4'}
