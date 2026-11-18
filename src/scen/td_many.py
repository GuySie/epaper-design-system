# the widest readings: 14 open items (one of 40 characters, due days up to a date) and 4 done
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/td.py').read())
OPEN = [('Take out the paper', -1), ('Water the plants on the balcony and in the hall', 0), ('Vacuum upstairs', 1), ('Clean the bathroom', 1), ('Descale the kettle', 12), ('Change the bed sheets', None), ('Mow the lawn', None), ('Fix the bike light', None), ('Sort the mail', None), ('Book the dentist', None), ('Clean the oven', None), ('Wash the car', None), ('Order printer ink', None), ('Oil the door hinge', None)]
DONE = ['Laundry', 'Dishes', 'Groceries', 'Bins']
TODO_RESPONSE = {E: {'items': items(OPEN, DONE)}}
STATES[E]['state'] = '14'
STATES[E]['attributes']['friendly_name'] = 'Chores'
DEVICE_NAMES[E] = 'Chores'
