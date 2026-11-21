# done three hours ago, the door still closed: severe (red)
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/ap.py').read())
STATES[S] = {'state': 'finished', 'attributes': {}, 'last_updated': NOW - dt.timedelta(hours=3)}; TRANSLATED[S] = 'Finished'
STATES[DR]['last_updated'] = NOW - dt.timedelta(hours=4)
EXPECT = ['DONE · DOOR STILL CLOSED']
EXPECT_FILL = 'red'
EXPECT_CHIP = 'red'      # the Glance secondary is the chip at the level (*Glance*, *Severity takes the Glance secondary*)
EXPECT_SHARE = 100
