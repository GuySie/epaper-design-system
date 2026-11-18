# another configuration: flagging off
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/td.py').read())
INPUTS['flag_due'] = False
