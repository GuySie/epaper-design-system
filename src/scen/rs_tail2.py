# a flagged word with a tail and a Glance secondary: the fill holds both
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/rs_tail.py').read())
STATES[E2]['state'] = 'Until 15:30'; TRANSLATED[E2] = 'Until 15:30'
INPUTS['secondary_entity'] = E2
EXPECT = ['Until 15:30']
EXPECT_BLOCK = True      # the hero block is the chip (*Glance with a word*, *Flagged*)
