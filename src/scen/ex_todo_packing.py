# an example of what the page is used for (README, lib/pictures.py): in English, on a BWRY panel
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/td.py').read())
OPEN = [('Passports', None), ('Chargers', None), ('Sunscreen', None)]
DONE = ['Tickets', 'Swimwear']
TODO_RESPONSE = {E: {'items': items(OPEN, DONE)}}
STATES[E]['attributes']['friendly_name'] = 'Packing'
DEVICE_NAMES[E] = 'Packing'
INPUTS.update({'weekday_format': 'en', 'displays': ['dev1']})
MODELS = {'dev1': 'BWRY'}
