# high, at warning
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/sv.py').read())
INPUTS.update({'flag_high': True, 'warning_high': 1000, 'severe_high': 1400})
