exec(open(__import__('os').environ['EP_ROOT'] + '/scen/appt_m.py').read())
CALENDAR_RESPONSE['calendar.work']['events'] = CALENDAR_RESPONSE['calendar.work']['events'][:3]
