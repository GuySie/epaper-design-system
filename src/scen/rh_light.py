exec(open(__import__('os').environ['EP_ROOT'] + '/scen/rh.py').read())
# light rain: nothing reaches the warning line, the footer is a statement
MM = [0, 0, 0, 0, 0, 0.4, 0.9, 1.2, 0.7, 0.2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
FORECASTS['weather.home']['hourly'] = hourly(MM, NOW)
