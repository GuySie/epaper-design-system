# 12-hour time: every axis label and the footer's span carry am/pm
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/rain35.py').read())
INPUTS.update({'time_format': '12h', 'weekday_format': 'en'})
