exec(open(__import__('os').environ['EP_ROOT'] + '/scen/appt_m.py').read())
# no events at all: the empty statement
CALENDAR_RESPONSE['calendar.work']['events'] = []
