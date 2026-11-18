# an example of what the page is used for (README, lib/pictures.py): in English, on a BWRY panel
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/tl.py').read())
ents = [('binary_sensor.w', 'off', '', 'Windows', 'Closed', '', 'mdi:window-closed-variant'), ('binary_sensor.b', 'on', '', 'Back door', 'Open', '', 'mdi:door-open'), ('sensor.l', '2', '', 'Lights on', '', '', ''),
        ('switch.s', 'off', '', 'Stove', 'Off', '', ''), ('switch.i', 'off', '', 'Iron', 'Off', '', ''), ('alarm_control_panel.a', 'disarmed', '', 'Alarm', 'Disarmed', '', 'mdi:home-lock')]
STATES = {e: S(s, u, n, own) for e, s, u, n, w, own, ic in ents}
TRANSLATED = {e: w for e, s, u, n, w, own, ic in ents if w}
DEVICE_NAMES = {e: d['attributes']['friendly_name'] for e, d in STATES.items()}
INPUTS = {'header_title': 'Before you leave'}
for i, (e, s, u, n, w, own, ic) in enumerate(ents, 1):
    INPUTS[f'entity_{i}'] = e
    if ic: INPUTS[f'entity_{i}_icon'] = ic
INPUTS.update({'weekday_format': 'en', 'displays': ['dev1']})
MODELS = {'dev1': 'BWRY'}
