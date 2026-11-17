import datetime as dt, math
TZ = dt.timezone(dt.timedelta(hours=1))
NOW = dt.datetime(2026, 8, 2, 20, 47, tzinfo=TZ)
E = 'sensor.studio_co2'
AREAS = {E: 'Studio'}
def series(hours=12, f=None, skip=()):
    out = []
    start = NOW.replace(minute=(NOW.minute // 5) * 5, second=0) - dt.timedelta(hours=hours)
    n = hours * 12
    for i in range(n):
        if i in skip: continue
        t = start + dt.timedelta(minutes=5 * i)
        v = f(i / n)
        out.append({'start': t.astimezone(dt.timezone.utc).isoformat(), 'end': (t + dt.timedelta(minutes=5)).astimezone(dt.timezone.utc).isoformat(), 'mean': v, 'max': v + 6})
    return out
def calm(x):  # evening in a room: rises while occupied, drops when the window opens
    return 470 + 380 * math.exp(-((x - 0.55) / 0.12) ** 2) + 120 * x
STATS_RESPONSE = {'statistics': {E: series(12, calm)}}
STATES = {E: {'state': '592', 'attributes': {'friendly_name': 'Studio CO2', 'unit_of_measurement': 'ppm', 'device_class': 'carbon_dioxide'}, 'last_updated': NOW - dt.timedelta(minutes=1)}}
INPUTS = {'co2_entity': E, 'displays': ['dev1'], 'weekday_format': 'nl'}
MODELS = {'dev1': 'Solum 3.5 BWR'}
