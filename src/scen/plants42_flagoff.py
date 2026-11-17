# the dry-soil switch off: no plant is flagged
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/plants42.py').read())
INPUTS['flag_moisture_low'] = False
