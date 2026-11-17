exec(open(__import__('os').environ['EP_ROOT'] + '/scen/wxp16.py').read())
INPUTS.update({'severe_pollen_high': 1000, 'warning_pollen_high': 500})
