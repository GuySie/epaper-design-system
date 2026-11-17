exec(open(__import__('os').environ['EP_ROOT'] + '/scen/tonight.py').read())
INPUTS.update({'time_format': '12h', 'weekday_format': 'en', 'header_title': 'Garden'})
