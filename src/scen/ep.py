# Energy price (EnergyZero): an ordinary afternoon; the evening passes the warning level and one hour is severe
import datetime as dt
TZ = dt.timezone(dt.timedelta(hours=1))
NOW = dt.datetime(2026, 8, 1, 14, 7, 30, tzinfo=TZ)
CT = [9, 8, 7, 7, 7, 8, 10, 13, 14, 12, 9, 8, 7, 7, 8, 10, 13, 16, 26, 17, 13, 11, 10, 9]


def prices(ct, now):
    """the action's response for today: an entry per hour from local midnight, in euros per kWh; None: no entry"""
    t0 = now.replace(hour=0, minute=0, second=0, microsecond=0).astimezone(dt.timezone.utc)
    out = []
    for i, c in enumerate(ct):
        if c is not None:
            a, b = t0 + dt.timedelta(hours=i), t0 + dt.timedelta(hours=i + 1)
            out.append({'price': c / 100, 'timestamp': str(a), 'start': str(a), 'end': str(b)})
    return {'prices': out}


def at(hour):
    return NOW.replace(hour=hour)


PRICE_RESPONSE = prices(CT, NOW)
STATES = {}
INPUTS = {'weekday_format': 'nl', 'energyzero_entry': 'entry-energyzero'}
