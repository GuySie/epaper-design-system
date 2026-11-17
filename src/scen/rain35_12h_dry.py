# 12-hour time, dry: the statement's time carries pm as a unit
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/rain_dry.py').read())
INPUTS.update({'time_format': '12h', 'weekday_format': 'en'})
