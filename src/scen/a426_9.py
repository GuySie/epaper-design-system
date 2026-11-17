exec(open(__import__('os').environ['EP_ROOT'] + '/scen/a41_6.py').read())
SIZE = (800, 480)
EV += [ev('2026-08-04T13:00:00+01:00', '2026-08-04T14:00:00+01:00', 'Lunch & learn: design tokens'),
       ev('2026-08-04T15:00:00+01:00', '2026-08-04T16:00:00+01:00', 'Logo critique'),
       ev('2026-08-04T16:30:00+01:00', '2026-08-04T17:00:00+01:00', 'Wrap-up')]
CALENDAR_RESPONSE = {'calendar.work': {'events': EV}}
