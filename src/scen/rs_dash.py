# a sign the hero face hasn't measured (an en dash): left out, and the spaces collapsed again
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/rs.py').read())
STATES[E]['state'] = 'Out – back soon'; TRANSLATED[E] = 'Out – back soon'
EXPECT_NOT = ['–', '  ']
EXPECT_BLOCK = False
