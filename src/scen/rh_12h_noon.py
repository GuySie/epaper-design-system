exec(open(__import__('os').environ['EP_ROOT'] + '/scen/rh.py').read())
# 12-hour time across noon, the widest footer: both ends of the span carry am/pm (Spanish, heavy rain)
NOW = dt.datetime(2026, 8, 1, 9, 7, 30, tzinfo=TZ)
STATES['weather.home']['last_updated'] = NOW - dt.timedelta(minutes=5)
MM = [0, 3, 12, 15, 20, 25, 30, 35, 40, 45, 50, 50, 45, 40, 35, 30, 25, 20, 15, 12, 11, 10.5, 10, 6]
FORECASTS['weather.home']['hourly'] = hourly(MM, NOW)
INPUTS.update({'time_format': '12h', 'weekday_format': 'es'})
