# a narrow reading, 11:11: the bar keeps its width (*Glance with a progress bar*, *The bar*)
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/ap.py').read())
STATES[EN]['state'] = NOW.replace(hour=11, minute=11).isoformat()
EXPECT = ['11:11']
EXPECT_SHARE = 62
