# Buienradar only: Buienalarm reports no data, so the bars come from the second source (its "code|HH:MM" text)
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/rain35.py').read())
_t0 = NOW.replace(second=0, microsecond=0)
_t0 = _t0.replace(minute=(_t0.minute // 5) * 5)
STATES['sensor.neerslag_buienalarm_regen_data']['attributes']['data'] = {'success': False}
STATES['sensor.neerslag_buienradar_regen_data']['attributes']['data'] = ' '.join(
    f"{c:03d}|{(_t0 + dt.timedelta(minutes=5 * i)).strftime('%H:%M')}" for i, c in enumerate(codes[:24]))
