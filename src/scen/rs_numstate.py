# a number as the state: drawn like any status (*Room sign*, *A number as the state*)
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/rs.py').read())
STATES[E] = {'state': '3', 'attributes': {'friendly_name': 'Study people'}, 'last_updated': NOW}
TRANSLATED[E] = '3'
EXPECT = ['3']
EXPECT_BLOCK = False
