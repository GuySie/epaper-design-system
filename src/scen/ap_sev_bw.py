# severe on a black/white panel: an ink chip, an ink bar
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/ap.py').read())
EXPECT = []
STATES[S] = {'state': 'finished', 'attributes': {}, 'last_updated': NOW - dt.timedelta(hours=3)}; TRANSLATED[S] = 'Finished'
STATES[DR]['last_updated'] = NOW - dt.timedelta(hours=4)
MODELS = {'dev1': 'X BW'}
EXPECT_FILL = 'black'
EXPECT_CHIP = 'black'      # the Glance secondary is the chip at the level (*Glance*, *Severity takes the Glance secondary*)
EXPECT_SHARE = 100
