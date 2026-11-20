# the switch off: tomorrow is plain text
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/bd_long.py').read())
INPUTS['flag_soon'] = False
