# done, the door sensor unavailable: as if there were none, DONE and not flagged (*Appliance run*, *Done*)
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/ap.py').read())
STATES[S] = {'state': 'finished', 'attributes': {}, 'last_updated': NOW - dt.timedelta(hours=3)}; TRANSLATED[S] = 'Finished'
STATES[DR]['state'] = 'unavailable'
EXPECT = ['DONE']
EXPECT_NOT = ['CLOSED', 'NOT RUNNING']
EXPECT_SHARE = 100
