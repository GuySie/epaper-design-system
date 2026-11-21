# an example of what the page is used for (README, lib/pictures.py): in English, on a BWRY panel
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/entities35.py').read())
ents = [('sensor.r1', '21.4', '°C', 'Living room'), ('sensor.r2', '20.8', '°C', 'Kitchen'), ('sensor.r3', '18.2', '°C', 'Bedroom'), ('sensor.r4', '19.6', '°C', 'Kids room'), ('sensor.r5', '22.9', '°C', 'Bathroom'),
        ('sensor.r6', '17.1', '°C', 'Attic'), ('sensor.r7', '19.9', '°C', 'Study'), ('sensor.r8', '18.7', '°C', 'Guest room'), ('sensor.r9', '16.4', '°C', 'Hallway'), ('sensor.r10', '12.3', '°C', 'Garage')]
STATES = {e: {'state': s, 'attributes': {'unit_of_measurement': u, 'friendly_name': n}} for e, s, u, n in ents}
INPUTS = {f'entity_{i+1}': e for i, (e, *_r) in enumerate(ents)}
INPUTS.update({f'entity_{i}': '' for i in range(len(ents)+1, 13)})
INPUTS['header_title'] = 'Temperatures'
INPUTS.update({'weekday_format': 'en', 'displays': ['dev1']})
MODELS = {'dev1': 'BWRY'}
