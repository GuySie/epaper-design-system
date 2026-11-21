# done 10 minutes ago, the door still closed, under the warning time: DONE, the bar full, the hero the time it turned done
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/ap.py').read())
STATES[S] = {'state': 'finished', 'attributes': {}, 'last_updated': NOW - dt.timedelta(minutes=10)}; TRANSLATED[S] = 'Finished'
EXPECT = ['DONE', '13:00']
EXPECT_SHARE = 100
EXPECT_NOT = ['CLOSED']
