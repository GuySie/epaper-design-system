# an example of what the page is used for (README, lib/pictures.py): in English, on a BWRY panel; a dishwasher done 30 minutes ago, its door still closed: a warning
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/ap.py').read())
STATES[S] = {'state': 'finished', 'attributes': {}, 'last_updated': NOW - dt.timedelta(minutes=30)}
STATES[PG]['state'] = 'eco_50'
TRANSLATED = {S: 'Finished', PG: 'Eco 50°'}
DEVICE_NAMES = {k: 'Dishwasher' for k in STATES}
INPUTS['icon'] = 'mdi:dishwasher'
EXPECT = ['DONE · DOOR STILL CLOSED']
EXPECT_SHARE = 100
MODELS = {'dev1': 'BWRY'}
