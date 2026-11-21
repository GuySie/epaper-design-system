# two bins tomorrow, one of them two words: each bin stays on one line, and the day still shows
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/bd_two.py').read())
INPUTS['bin_2_label'] = 'Residual waste'
EXPECT = ['TOMORROW']
