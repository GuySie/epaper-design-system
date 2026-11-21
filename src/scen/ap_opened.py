# done, and the door opened since: not running (*Appliance run*, *Done*)
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/ap.py').read())
STATES[S] = {'state': 'finished', 'attributes': {}, 'last_updated': NOW - dt.timedelta(minutes=30)}; TRANSLATED[S] = 'Finished'
STATES[DR] = {'state': 'on', 'attributes': {'device_class': 'door'}, 'last_updated': NOW - dt.timedelta(minutes=5)}
STATES[S]['state'] = 'finished'
EXPECT = ['NOT RUNNING']
EXPECT_SHARE = None
NO_BLOCK = True      # not running or the error state: no hero block to keep in place
