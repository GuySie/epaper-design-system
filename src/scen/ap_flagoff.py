# done and not emptied, flagging off: DONE, never a chip
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/ap.py').read())
STATES[S] = {'state': 'finished', 'attributes': {}, 'last_updated': NOW - dt.timedelta(hours=3)}; TRANSLATED[S] = 'Finished'
STATES[DR]['last_updated'] = NOW - dt.timedelta(hours=4)
INPUTS['flag_unemptied'] = False
EXPECT = ['DONE']
EXPECT_NOT = ['CLOSED']
EXPECT_SHARE = 100
