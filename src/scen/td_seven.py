# seven open items and no done ones on a landscape screen: two columns, not full
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/td.py').read())
OPEN = [('Take out the paper', -1), ('Water the plants', 0), ('Vacuum upstairs', 1), ('Clean the bathroom', 1), ('Change the bed sheets', None), ('Mow the lawn', None), ('Fix the bike light', None)]
DONE = []
TODO_RESPONSE = {E: {'items': items(OPEN, DONE)}}
STATES = {E: {'state': str(len(OPEN)), 'attributes': {'friendly_name': 'Chores'}, 'last_updated': NOW - dt.timedelta(minutes=2)}}
DEVICE_NAMES = {E: 'Chores'}
INPUTS = dict(INPUTS, weekday_format='en')
