exec(open(__import__('os').environ['EP_ROOT'] + '/scen/rh.py').read())
# the widest reading: the heaviest bar at the top of the scale (50 mm/h), severe across most of the day, and the
# longest footer (Spanish, 24-hour times: LLUVIA FUERTE ... PICO 50)
MM = [0, 3, 12, 15, 20, 25, 30, 35, 40, 45, 50, 50, 45, 40, 35, 30, 25, 20, 15, 12, 11, 10.5, 10, 6]
FORECASTS['weather.home']['hourly'] = hourly(MM, NOW)
INPUTS['weekday_format'] = 'es'
INPUTS['time_format'] = '24h'
