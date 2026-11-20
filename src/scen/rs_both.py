# a state in both lists: severe wins
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/rs.py').read())
INPUTS.update({'warning_states': ['Free'], 'severe_states': ['free']})
