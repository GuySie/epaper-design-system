# another configuration: thresholds set, both switches off
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/vd_sev.py').read())
INPUTS.update({'flag_high': False})
