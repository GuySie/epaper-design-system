# both switches off (the default): nothing is flagged, no lines
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/hg_both.py').read())
INPUTS.update({'flag_high': False, 'flag_low': False})
