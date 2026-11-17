import datetime as dt, math
TZ = dt.timezone(dt.timedelta(hours=1))
NOW = dt.datetime(2026, 8, 1, 14, 7, 30, tzinfo=TZ)
SIZE = (384, 184)
MM = [0, 0, 0, 0, 0.3, 0.8, 1.5, 3, 6, 11, 13, 8, 4, 2, 1, 0.5, 0.3, 0.2, 0.1, 0, 0, 0, 0, 0, 0, 0]
start = (int(NOW.timestamp()) // 300) * 300
codes = [0 if m <= 0 else round(109 + 32 * math.log10(m)) for m in MM]
STATES = {
    'sensor.neerslag_buienalarm_regen_data': {'state': 'ok', 'attributes': {'data': {'success': True, 'start': start, 'delta': 300, 'precip': codes}},
                                             'last_updated': NOW - dt.timedelta(minutes=3)},
    'sensor.neerslag_buienradar_regen_data': {'state': 'ok', 'attributes': {'data': ''}, 'last_updated': NOW - dt.timedelta(minutes=4)},
}
INPUTS = {'weekday_format': 'nl'}
