# the status unavailable: the error state (*Appliance run*, *Unavailable*)
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/ap.py').read())
STATES[S]['state'] = 'unavailable'
EXPECT = ['APPLIANCE UNAVAILABLE']
EXPECT_SHARE = None
NO_BLOCK = True      # not running or the error state: no hero block to keep in place
