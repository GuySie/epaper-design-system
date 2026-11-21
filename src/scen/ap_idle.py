# not running: one empty statement (*Appliance run*, *Not running*)
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/ap.py').read())
STATES[S] = {'state': 'inactive', 'attributes': {}, 'last_updated': NOW - dt.timedelta(hours=5)}; TRANSLATED[S] = 'Inactive'
EXPECT = ['NOT RUNNING']
EXPECT_SHARE = None
NO_BLOCK = True      # not running or the error state: no hero block to keep in place
