# one word too long for the smallest rung: cut with an ellipsis
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/rs.py').read())
STATES[E]['state'] = 'Maintenance'; TRANSLATED[E] = 'Maintenance'
INPUTS['warning_states'] = ['Maintenance']
EXPECT_BLOCK = True      # the hero block is the chip (*Glance with a word*, *Flagged*)
