# high: the period reaches warning, not severe
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/hg.py').read())
INPUTS.update({'flag_high': True, 'warning_high': 22, 'severe_high': 23.5})
