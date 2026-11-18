exec(open(__import__('os').environ['EP_ROOT'] + '/scen/rh_dry.py').read())
# 12-hour time, dry: the statement's weekday and time as the update stamp writes them
INPUTS.update({'time_format': '12h', 'weekday_format': 'en'})
