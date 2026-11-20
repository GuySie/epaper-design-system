# a flagged word with an accent: the chip covers it
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/rs_busy.py').read())
STATES[E]['state'] = 'Occupé'; TRANSLATED[E] = 'Occupé'
INPUTS['severe_states'] = ['occupé']
