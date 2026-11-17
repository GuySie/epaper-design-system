exec(open(__import__('os').environ['EP_ROOT'] + '/scen/wxp16.py').read())
INPUTS.update({'warning_conditions': ['cloudy', 'partlycloudy'], 'severe_conditions': ['rainy', 'pouring', 'lightning-rainy'], 'displays': ['d1']})
MODELS = {'d1': 'X BWRY'}
