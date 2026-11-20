# a number as the state: drawn as reported, without a unit
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/rs.py').read())
STATES[E] = {'state': '3', 'attributes': {'friendly_name': 'Study people', 'unit_of_measurement': 'people'}, 'last_updated': NOW}
TRANSLATED[E] = '3'
