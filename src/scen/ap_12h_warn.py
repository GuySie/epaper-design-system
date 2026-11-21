# 12-hour time when flagged: pm stays beside the hero (*Appliance run*, *12-hour time*)
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/ap.py').read())
STATES[S] = {'state': 'finished', 'attributes': {}, 'last_updated': NOW - dt.timedelta(minutes=30)}; TRANSLATED[S] = 'Finished'
INPUTS['time_format'] = '12h'
EXPECT = ['12:40', 'pm', 'DONE · DOOR STILL CLOSED']
EXPECT_SHARE = 100
