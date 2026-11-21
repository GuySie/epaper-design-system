# three words on two lines with a Glance secondary, not flagged: the same places as flagged
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/rs_long2.py').read())
INPUTS['severe_states'] = []
EXPECT_BLOCK = False      # the hero block is the chip (*Glance with a word*, *Flagged*)
