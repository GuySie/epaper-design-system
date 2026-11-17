# Weather and calendar: values the weather entity doesn't report show —
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/wxag.py').read())
for _k in ('humidity', 'pressure', 'wind_speed'):
    STATES['weather.home']['attributes'].pop(_k, None)
