# a flagged word with a tail (Q): the tail stays inside the fill
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/rs.py').read())
STATES[E]['state'] = 'Quiet'; TRANSLATED[E] = 'Quiet'
INPUTS['warning_states'] = ['Quiet']
EXPECT_BLOCK = True      # the hero block is the chip (*Glance with a word*, *Flagged*)
