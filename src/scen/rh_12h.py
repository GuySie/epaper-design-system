exec(open(__import__('os').environ['EP_ROOT'] + '/scen/rh.py').read())
# 12-hour time: every axis label and the footer's span carry am/pm
INPUTS.update({'time_format': '12h', 'weekday_format': 'en'})
