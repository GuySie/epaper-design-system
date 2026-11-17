exec(open(__import__('os').environ['EP_ROOT'] + '/scen/med_warn.py').read())
INPUTS['displays'] = ['g1']
MODELS = {'g1': '2.7" GRAYSCALE_4'}
