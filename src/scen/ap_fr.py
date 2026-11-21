# the French chip: cut with an ellipsis where it doesn't fit (*Appliance run*, *Done*)
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/ap.py').read())
STATES[S] = {'state': 'finished', 'attributes': {}, 'last_updated': NOW - dt.timedelta(hours=3)}; TRANSLATED[S] = 'Finished'
STATES[DR]['last_updated'] = NOW - dt.timedelta(hours=4)
INPUTS['weekday_format'] = 'fr'
EXPECT = ['TERMINÉ', '...']
EXPECT_SHARE = 100
