# do not disturb on a black/white panel: two lines in an ink block
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/rs_long.py').read())
MODELS = {'dev1': 'X BW'}
EXPECT_BLOCK = True      # the hero block is the chip (*Glance with a word*, *Flagged*)
