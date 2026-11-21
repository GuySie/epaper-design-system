# done 30 minutes ago, the door still closed: a warning (an outlined chip, an ink bar: no warning colour on this panel) (*Appliance run*, *Flagged*)
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/ap.py').read())
STATES[S] = {'state': 'finished', 'attributes': {}, 'last_updated': NOW - dt.timedelta(minutes=30)}; TRANSLATED[S] = 'Finished'
EXPECT = ['DONE · DOOR STILL CLOSED']
EXPECT_FILL = 'black'
EXPECT_CHIP = 'outline'      # the Glance secondary is the chip at the level (*Glance*, *Severity takes the Glance secondary*)
EXPECT_SHARE = 100
