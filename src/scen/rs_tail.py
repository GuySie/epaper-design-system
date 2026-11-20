# a flagged word with a tail (Q): the chip covers it
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/rs.py').read())
STATES[E]['state'] = 'Quiet'; TRANSLATED[E] = 'Quiet'
INPUTS['warning_states'] = ['Quiet']
