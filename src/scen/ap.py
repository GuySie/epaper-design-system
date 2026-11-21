# Appliance run: a washing machine running Eco 40°, 62 % done, ending at 14:32 (the ordinary reading)
import datetime as dt
TZ = dt.timezone(dt.timedelta(hours=1))
NOW = dt.datetime(2026, 8, 3, 13, 10, tzinfo=TZ)
S, EN, PR, PG, DR = 'sensor.washer_status', 'sensor.washer_finish', 'sensor.washer_progress', 'sensor.washer_programme', 'binary_sensor.washer_door'
STATES = {S: {'state': 'run', 'attributes': {}, 'last_updated': NOW - dt.timedelta(minutes=80)},
          EN: {'state': (NOW + dt.timedelta(minutes=82)).isoformat(), 'attributes': {'device_class': 'timestamp'}, 'last_updated': NOW - dt.timedelta(minutes=5)},
          PR: {'state': '62', 'attributes': {'unit_of_measurement': '%'}, 'last_updated': NOW - dt.timedelta(minutes=2)},
          PG: {'state': 'eco_40', 'attributes': {}, 'last_updated': NOW - dt.timedelta(minutes=80)},
          DR: {'state': 'off', 'attributes': {'device_class': 'door'}, 'last_updated': NOW - dt.timedelta(minutes=85)}}
TRANSLATED = {S: 'Running', PG: 'Eco 40°'}
DEVICE_NAMES = {S: 'Washing machine', EN: 'Washing machine', PR: 'Washing machine', PG: 'Washing machine', DR: 'Washing machine'}
INPUTS = {'displays': ['dev1'], 'weekday_format': 'en', 'status_entity': S, 'end_entity': EN, 'progress_entity': PR, 'programme_entity': PG, 'door_entity': DR, 'icon': 'mdi:washing-machine'}
EXPECT = ['Eco 40', '62']     # the programme as written (*Text rules*, rule 0)
EXPECT_SHARE = 62               # the bar filled to the share done
