# no end time: the hero is a dash, without its icon (*Appliance run*, *Running*)
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/ap.py').read())
STATES[EN]['state'] = 'unavailable'
EXPECT = ['—', '62']
EXPECT_ICON = False   # the dash has no icon
EXPECT_SHARE = 62
