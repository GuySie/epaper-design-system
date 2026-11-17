exec(open(__import__('os').environ['EP_ROOT'] + '/scen/wxp29v.py').read())
INPUTS.update({'warning_conditions': ['rainy'], 'severe_conditions': ['pouring'], 'displays': ['d1']})
MODELS = {'d1': 'X BWRY'}
