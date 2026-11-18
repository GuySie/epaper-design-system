exec(open(__import__('os').environ['EP_ROOT'] + '/scen/rh.py').read())
# a dry day, the empty statement: its end is a day away, so it carries its weekday
FORECASTS['weather.home']['hourly'] = hourly([0], NOW)
