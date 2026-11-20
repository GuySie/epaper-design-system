# Bin day: paper and plastic on the same day, tomorrow: two words stacked
import datetime as dt
TZ = dt.timezone(dt.timedelta(hours=1))
NOW = dt.datetime(2026, 8, 1, 14, 10, tzinfo=TZ)
def D(days): return (NOW + dt.timedelta(days=days)).strftime('%Y-%m-%d')
def S(days, name): return {'state': D(days), 'attributes': {'friendly_name': name, 'device_class': 'date'}, 'last_updated': NOW - dt.timedelta(minutes=2)}
STATES = {'sensor.bin_paper': S(1, 'Paper'), 'sensor.bin_plastic': S(1, 'Plastic'), 'sensor.bin_organic': S(12, 'Organic'), 'sensor.bin_rest': S(20, 'Residual waste')}
DEVICE_NAMES = {k: v['attributes']['friendly_name'] for k, v in STATES.items()}
INPUTS = {'displays': ['dev1'], 'weekday_format': 'en', 'bin_1': 'sensor.bin_paper', 'bin_1_label': 'Paper', 'bin_1_icon': 'mdi:newspaper-variant-outline', 'bin_2': 'sensor.bin_plastic', 'bin_2_label': 'Plastic', 'bin_2_icon': 'mdi:bottle-soda-outline', 'bin_3': 'sensor.bin_organic', 'bin_3_label': 'Organic', 'bin_3_icon': 'mdi:leaf', 'bin_4': 'sensor.bin_rest', 'bin_4_label': 'Residual waste', 'bin_4_icon': 'mdi:trash-can-outline'}
