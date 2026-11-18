# both switches off (the default): nothing is flagged
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/lv_sev.py').read())
INPUTS['flag_low'] = False
