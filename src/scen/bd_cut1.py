# one word too long for the smallest rung: cut with an ellipsis
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/bd.py').read())
STATES['sensor.bin_rest']['state'] = D(2)
INPUTS['bin_4_label'] = 'Christmastrees'
