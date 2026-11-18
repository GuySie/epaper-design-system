# an example of what the page is used for (README, lib/pictures.py): in English, on a BWRY panel
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/entities35.py').read())
ents = [('sensor.p1', 'Out for delivery', '', 'Bookshop'), ('sensor.p2', 'In transit', '', 'Bike parts'), ('sensor.p3', 'At the pick-up point', '', 'Pharmacy'), ('sensor.p4', 'Delivered', '', 'Garden centre')]
STATES = {e: {'state': s, 'attributes': {'unit_of_measurement': u, 'friendly_name': n}} for e, s, u, n in ents}
INPUTS = {f'entity_{i+1}': e for i, (e, *_r) in enumerate(ents)}
INPUTS.update({f'entity_{i}': '' for i in range(len(ents)+1, 13)})
INPUTS['header_title'] = 'Packages'
INPUTS.update({'weekday_format': 'en', 'displays': ['dev1']})
MODELS = {'dev1': 'BWRY'}
