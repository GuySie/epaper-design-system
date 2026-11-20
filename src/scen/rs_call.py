# Room sign: in a call: a warning, a longer word that steps down
import datetime as dt
TZ = dt.timezone(dt.timedelta(hours=1))
NOW = dt.datetime(2026, 8, 3, 14, 10, tzinfo=TZ)
E, E2 = 'input_select.study_status', 'sensor.study_free_at'
STATES = {E: {'state': 'In a call', 'attributes': {'friendly_name': 'Study status'}, 'last_updated': NOW - dt.timedelta(hours=2)},
          E2: {'state': 'Until 15:30', 'attributes': {'friendly_name': 'Study free at'}, 'last_updated': NOW - dt.timedelta(hours=2)}}
TRANSLATED = {E: 'In a call', E2: 'Until 15:30'}
AREAS = {E: 'Study', E2: 'Study'}
DEVICE_NAMES = {E: 'Study status', E2: 'Study free at'}
INPUTS = dict({'entity': E, 'displays': ['dev1'], 'weekday_format': 'en', 'warning_states': ['In a call'], 'severe_states': ['Busy', 'Do not disturb']}, **{'secondary_entity': 'sensor.study_free_at'})
