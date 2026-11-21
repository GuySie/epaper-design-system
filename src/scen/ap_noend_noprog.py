# no end time and no progress sensor: a dash, the bar empty (*Appliance run*, *Running*)
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/ap.py').read())
STATES[EN]['state'] = 'unknown'
INPUTS['progress_entity'] = ''
EXPECT = ['—']
EXPECT_ICON = False
EXPECT_SHARE = 0
