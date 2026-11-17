# the event hero's widest reading: 20:00
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/a41_6.py').read())
EV = [ev('2026-08-03T20:00:00+01:00', '2026-08-03T22:00:00+01:00', 'Heron team dinner')]
CALENDAR_RESPONSE = {'calendar.work': {'events': EV}}
