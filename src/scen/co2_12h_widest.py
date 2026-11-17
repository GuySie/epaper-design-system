# 12-hour time with the widest reading (4000)
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/co2_widest.py').read())
INPUTS.update({'time_format': '12h', 'weekday_format': 'en'})
