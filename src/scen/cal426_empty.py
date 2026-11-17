# the 4.26": no events at all in the days shown
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/cal426.py').read())
CALENDAR_RESPONSE['calendar.home']['events'] = []
