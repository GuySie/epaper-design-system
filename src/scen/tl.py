# Tiles: twelve entities; icons from the input, from the entity, and one tile without
import datetime as dt
TZ = dt.timezone(dt.timedelta(hours=1))
NOW = dt.datetime(2026, 8, 1, 14, 10, tzinfo=TZ)
# entity, state, unit, name, Home Assistant's wording, the entity's own icon, the icon input
ents = [('binary_sensor.window', 'on', '', 'Windows', 'Open', '', 'mdi:window-open'), ('binary_sensor.front_door', 'off', '', 'Front door', 'Closed', '', 'mdi:door-closed'),
        ('sensor.living', '21.4', '°C', 'Living', '', 'mdi:thermometer', ''), ('sensor.washer', 'done', '', 'Washer', 'Done', 'mdi:washing-machine', ''),
        ('sensor.lights', '3', '', 'Lights on', '', '', ''), ('alarm_control_panel.home', 'armed_away', '', 'Alarm', 'Armed away', '', 'mdi:shield-home'),
        ('cover.garage', 'closed', '', 'Garage', 'Closed', 'mdi:garage', ''), ('sensor.humidity', '48', '%', 'Humidity', '', 'mdi:water-percent', ''),
        ('sensor.car', '82', '%', 'Car', '', '', 'mdi:car-electric'), ('sensor.bins', 'paper', '', 'Bins', 'Paper', '', 'mdi:trash-can-outline'),
        ('sensor.dishwasher', 'running', '', 'Dishwasher', 'Running', 'mdi:dishwasher', ''), ('sensor.solar', '1.8', 'kW', 'Solar', '', 'mdi:solar-power', '')]
def S(state, unit, name, icon):
    a = {'friendly_name': name}
    if unit: a['unit_of_measurement'] = unit
    if icon: a['icon'] = icon
    return {'state': state, 'attributes': a, 'last_updated': NOW - dt.timedelta(minutes=2)}
STATES = {e: S(s, u, n, own) for e, s, u, n, w, own, ic in ents}
TRANSLATED = {e: w for e, s, u, n, w, own, ic in ents if w}
DEVICE_NAMES = {e: d['attributes']['friendly_name'] for e, d in STATES.items()}
INPUTS = {'displays': ['dev1'], 'weekday_format': 'nl'}
for i, (e, s, u, n, w, own, ic) in enumerate(ents, 1):
    INPUTS[f'entity_{i}'] = e
    if ic: INPUTS[f'entity_{i}_icon'] = ic
