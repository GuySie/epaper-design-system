# values the weather entity doesn't report (humidity, pressure, wind): each shows — and its label stays
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/wx.py').read())
for _k in ('humidity', 'pressure', 'wind_speed'):
    STATES['weather.home']['attributes'].pop(_k, None)
