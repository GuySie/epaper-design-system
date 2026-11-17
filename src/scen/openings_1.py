import datetime as dt
TZ = dt.timezone(dt.timedelta(hours=1))
NOW = dt.datetime(2026, 8, 3, 8, 5, tzinfo=TZ)
MODELS = {'dev1': '1.4" BWRY'}
def S(state, dc, name): return {'state': state, 'attributes': {'device_class': dc, 'friendly_name': name}}
STATES = {
 'binary_sensor.hallway_front_door': S('off', 'opening', 'Aqara Front Door Sensor'),
 'binary_sensor.bedroom_window': S('on', 'window', 'Window'),
 'binary_sensor.living_room_balcony_door': S('off', 'opening', 'Aqara Balcony Door Sensor'),
 'binary_sensor.kitchen_window': S('off', 'opening', 'Aqara Window Sensor'),
}
AREAS = {'binary_sensor.hallway_front_door': 'Hallway', 'binary_sensor.bedroom_window': 'Bedroom',
         'binary_sensor.living_room_balcony_door': 'Living Room', 'binary_sensor.kitchen_window': 'Kitchen'}
INPUTS = {'displays': ['dev1'], 'openings': list(STATES), 'severe_openings': ['binary_sensor.hallway_front_door'], 'weekday_format': 'nl'}
