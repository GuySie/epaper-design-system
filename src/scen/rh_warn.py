exec(open(__import__('os').environ['EP_ROOT'] + '/scen/rh.py').read())
# rain past the warning line (2.5 mm/h) that stays under severe (10 mm/h)
MM = [0, 0, 0.3, 0.8, 1.5, 2.6, 4, 6, 7, 5, 3, 2, 1, 0.5, 0.3, 0, 0, 0, 0, 0, 0, 0, 0, 0]
FORECASTS['weather.home']['hourly'] = hourly(MM, NOW)
