# the word with a tail, not flagged: it sits where the flagged one does
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/rs_tail.py').read())
INPUTS['warning_states'] = []
EXPECT_BLOCK = False
