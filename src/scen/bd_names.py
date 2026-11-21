# no words given: the sensors' names are the words
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/bd.py').read())
for n in range(1, 5): INPUTS['bin_%d_label' % n] = ''
STATES['sensor.bin_paper']['attributes']['friendly_name'] = 'Paper  ✂'; DEVICE_NAMES['sensor.bin_paper'] = 'Paper  ✂'
EXPECT_NOT = ['✂', '  ']
EXPECT = ['PAPER']
