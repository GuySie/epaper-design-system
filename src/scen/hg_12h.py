# 12-hour time, English
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/hg.py').read())
INPUTS.update({'time_format': '12h', 'weekday_format': 'en'})
