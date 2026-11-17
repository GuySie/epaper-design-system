# the usage switch off: a bar at 100 % is not flagged
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/claude35_sev.py').read())
INPUTS['flag_usage'] = False
