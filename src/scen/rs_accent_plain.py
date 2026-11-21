# the accented word, not flagged: it sits where the flagged one does (nothing moves when it is flagged)
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/rs_accent.py').read())
INPUTS['severe_states'] = []
EXPECT_BLOCK = False      # the hero block is the chip (*Glance with a word*, *Flagged*)
