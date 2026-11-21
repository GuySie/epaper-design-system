# emptied and the door shut again while the status stays done: not emptied again, flagged at once (*Appliance run*, *Done*)
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/ap.py').read())
STATES[S] = {'state': 'finished', 'attributes': {}, 'last_updated': NOW - dt.timedelta(minutes=30)}; TRANSLATED[S] = 'Finished'
STATES[DR] = {'state': 'off', 'attributes': {'device_class': 'door'}, 'last_updated': NOW - dt.timedelta(minutes=2)}
EXPECT = ['DONE · DOOR STILL CLOSED']
EXPECT_SHARE = 100
