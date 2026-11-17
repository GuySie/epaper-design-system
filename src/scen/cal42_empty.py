# no events at all in the days shown
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/cal42.py').read())
CALENDAR_RESPONSE['calendar.home']['events'] = []
