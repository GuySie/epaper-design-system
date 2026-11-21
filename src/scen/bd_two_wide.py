# two bins tomorrow, one word too long for the smallest rung: the day still shows
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/bd_two.py').read())
INPUTS['bin_2_label'] = 'Christmastrees'
EXPECT = ['TOMORROW']
