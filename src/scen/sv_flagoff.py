# both switches off (the default): a reading past the values is not flagged
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/sv_sev.py').read())
INPUTS['flag_high'] = False
