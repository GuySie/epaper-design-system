exec(open(__import__('os').environ['EP_ROOT'] + '/scen/wx75p.py').read())
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/_calendar.py').read())
# an empty day: Sunday 2 August has no events
CALENDAR_RESPONSE['calendar.home']['events'] = [e for e in CALENDAR_RESPONSE['calendar.home']['events'] if not e['start'].startswith('2026-08-02')]
