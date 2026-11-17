exec(open(__import__('os').environ['EP_ROOT'] + '/scen/wx75p.py').read())
CALENDAR_FROM = 'cal_m'
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/_calendar.py').read())
NOW = CAL_NOW                      # a fortnight of events: the calendar overflows
for _k in ('last_updated', 'last_reported'):
    STATES['weather.home'][_k] = NOW         # the weather reported at the calendar scenario's time too (not stale)
