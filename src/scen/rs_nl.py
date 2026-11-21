# Dutch wording of a state, with a second line
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/rs_busy.py').read())
STATES[E]['state'] = 'Bezet'; TRANSLATED[E] = 'Bezet'; TRANSLATED[E2] = 'Tot 15:30'
INPUTS.update({'weekday_format': 'nl', 'severe_states': ['bezet']})
EXPECT_BLOCK = True      # the hero block is the chip (*Glance with a word*, *Flagged*)
