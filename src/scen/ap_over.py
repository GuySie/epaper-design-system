# a progress sensor above 100: the percentage is at most 100% (*Appliance run*, *Running*)
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/ap.py').read())
STATES[PR]['state'] = '104'
EXPECT = ['100']
EXPECT_NOT = ['104']
EXPECT_SHARE = 100
