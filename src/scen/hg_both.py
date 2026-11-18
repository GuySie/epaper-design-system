# high and low on
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/hg.py').read())
INPUTS.update({'flag_high': True, 'warning_high': 21.5, 'severe_high': 22.5})
INPUTS.update({'flag_low': True, 'warning_low': 19.5, 'severe_low': 18.8})
