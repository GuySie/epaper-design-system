exec(open(__import__('os').environ['EP_ROOT'] + '/scen/sun35.py').read())
NOW = dt.datetime(2026, 6, 21, 16, 0, tzinfo=dt.timezone(dt.timedelta(hours=2)))
STATES['sun.sun']['attributes'].update(azimuth=245, elevation=42)
