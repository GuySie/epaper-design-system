# an example of what the page is used for (README, lib/pictures.py): in English, on a BWRY panel
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/entities35.py').read())
ents = [('sensor.s1', '12', '%', 'Processor'), ('sensor.s2', '48', '%', 'Memory'), ('sensor.s3', '71', '%', 'Disk'), ('sensor.s4', '41', '°C', 'Temperature'), ('sensor.s5', '92', 'Mbit/s', 'Download'), ('sensor.s6', '34', 'd', 'Running for')]
STATES = {e: {'state': s, 'attributes': {'unit_of_measurement': u, 'friendly_name': n}} for e, s, u, n in ents}
INPUTS = {f'entity_{i+1}': e for i, (e, *_r) in enumerate(ents)}
INPUTS.update({f'entity_{i}': '' for i in range(len(ents)+1, 13)})
INPUTS['header_title'] = 'Server'
INPUTS.update({'weekday_format': 'en', 'displays': ['dev1']})
MODELS = {'dev1': 'BWRY'}
