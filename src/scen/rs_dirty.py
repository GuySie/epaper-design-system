# a title, a state and a Glance secondary with characters the fonts lack and double spaces: sanitised, and the word keeps only measured characters
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/rs.py').read())
STATES[E]['state'] = '🔴 In  a call'; TRANSLATED[E] = '🔴 In  a call'
AREAS[E] = '🔴 Study  room'
STATES[E2]['state'] = '⏰ Until  15:30'; TRANSLATED[E2] = '⏰ Until  15:30'
INPUTS['secondary_entity'] = E2
EXPECT_NOT = ['🔴', '⏰', '  ']
EXPECT = ['CALL', 'Until 15:30']      # on the 1.4" the status breaks over two lines
EXPECT_BLOCK = True      # the hero block is the chip (*Glance with a word*, *Flagged*)
