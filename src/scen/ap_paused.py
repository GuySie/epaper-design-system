# a paused run counts as running (its state is in the running list)
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/ap.py').read())
STATES[S]['state'] = 'pause'; TRANSLATED[S] = 'Paused'
EXPECT = ['14:32', '62']
EXPECT_SHARE = 62
