# a number as the second entity: the room's temperature with its unit
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/rs.py').read())
STATES[E2] = {'state': '21.4', 'attributes': {'friendly_name': 'Study temperature', 'unit_of_measurement': '°C'}, 'last_updated': NOW}
TRANSLATED[E2] = '21.4'
INPUTS['secondary_entity'] = E2
