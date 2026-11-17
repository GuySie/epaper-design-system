# the 4.26": values the weather entity doesn't report show —
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/w426.py').read())
for _k in ('humidity', 'pressure', 'wind_speed'):
    STATES['weather.home']['attributes'].pop(_k, None)
