# History graph: a room's temperature over 12 hours
import datetime as dt, math
TZ = dt.timezone(dt.timedelta(hours=1))
NOW = dt.datetime(2026, 8, 1, 20, 47, tzinfo=TZ)
E = 'sensor.living_room_temp'
def series(hours, f, spread=0.2):
    out = []
    start = NOW.replace(minute=(NOW.minute // 5) * 5, second=0) - dt.timedelta(hours=hours)
    n = hours * 12
    for i in range(n):
        t = start + dt.timedelta(minutes=5 * i); v = f(i / n)
        out.append({'start': t.astimezone(dt.timezone.utc).isoformat(), 'end': (t + dt.timedelta(minutes=5)).astimezone(dt.timezone.utc).isoformat(), 'mean': v, 'max': v + spread, 'min': v - spread})
    return out
def day(x):  # a room over a day: cool in the morning, warm in the afternoon
    return 20.4 + 2.2 * math.exp(-((x - 0.6) / 0.18) ** 2) - 1.9 * math.exp(-((x - 0.2) / 0.1) ** 2)
STATS_RESPONSE = {'statistics': {E: series(12, day)}}
STATES = {E: {'state': '20.6', 'attributes': {'friendly_name': 'Living room temperature', 'unit_of_measurement': '°C'}, 'last_updated': NOW - dt.timedelta(minutes=1)}}
DEVICE_NAMES = {E: 'Living room temperature'}
INPUTS = {'entity': E, 'displays': ['dev1'], 'weekday_format': 'nl'}
