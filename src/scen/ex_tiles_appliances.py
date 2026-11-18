# an example of what the page is used for (README, lib/pictures.py): in English, on a BWRY panel
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/tl.py').read())
ents = [('sensor.a1', 'running', '', 'Washer', 'Running', 'mdi:washing-machine', ''), ('sensor.a2', 'done', '', 'Dryer', 'Done', 'mdi:tumble-dryer', ''), ('sensor.a3', 'off', '', 'Dishwasher', 'Off', 'mdi:dishwasher', ''),
        ('sensor.a4', '180', '°C', 'Oven', '', 'mdi:stove', ''), ('vacuum.a5', 'docked', '', 'Vacuum', 'Docked', 'mdi:robot-vacuum', ''), ('sensor.a6', '82', '%', 'Car', '', 'mdi:car-electric', '')]
STATES = {e: S(s, u, n, own) for e, s, u, n, w, own, ic in ents}
TRANSLATED = {e: w for e, s, u, n, w, own, ic in ents if w}
DEVICE_NAMES = {e: d['attributes']['friendly_name'] for e, d in STATES.items()}
INPUTS = {'header_title': 'Appliances'}
for i, (e, s, u, n, w, own, ic) in enumerate(ents, 1):
    INPUTS[f'entity_{i}'] = e
INPUTS.update({'weekday_format': 'en', 'displays': ['dev1']})
MODELS = {'dev1': 'BWRY'}
