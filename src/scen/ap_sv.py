# the Swedish chip, the longest translation: cut on every screen (*Appliance run*, *Done*)
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/ap.py').read())
STATES[S] = {'state': 'finished', 'attributes': {}, 'last_updated': NOW - dt.timedelta(minutes=30)}; TRANSLATED[S] = 'Finished'
INPUTS['weekday_format'] = 'sv'
EXPECT = ['KLAR', '...']
EXPECT_SHARE = 100
