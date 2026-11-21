# the warning on a panel with a warning colour: a yellow chip, a yellow bar
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/ap.py').read())
STATES[S] = {'state': 'finished', 'attributes': {}, 'last_updated': NOW - dt.timedelta(minutes=30)}; TRANSLATED[S] = 'Finished'
MODELS = {'dev1': '3.5" BWRY'}
EXPECT = ['DONE · DOOR STILL CLOSED']
EXPECT_FILL = 'yellow'
EXPECT_CHIP = 'yellow'      # the Glance secondary is the chip at the level (*Glance*, *Severity takes the Glance secondary*)
EXPECT_SHARE = 100
