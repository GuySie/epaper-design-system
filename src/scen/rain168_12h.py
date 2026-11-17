# 12-hour time on the 2.7": the axis writes PM in capitals (its label cut allows no lowercase)
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/rain168.py').read())
INPUTS.update({'time_format': '12h', 'weekday_format': 'en'})
