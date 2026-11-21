# a flagged word with an accent: the accent hangs above the fill
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/rs_busy.py').read())
STATES[E]['state'] = 'Occupé'; TRANSLATED[E] = 'Occupé'
INPUTS['severe_states'] = ['occupé']
EXPECT_BLOCK = True      # the hero block is the chip (*Glance with a word*, *Flagged*)
