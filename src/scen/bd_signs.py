# a bin word of signs only: the sensor's name instead
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/bd.py').read())
INPUTS['bin_1_label'] = '♻️'
EXPECT = ['PAPER']
