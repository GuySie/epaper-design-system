exec(open(__import__('os').environ['EP_ROOT'] + '/scen/a41_6.py').read())
EV = EV[1:1+0]
CALENDAR_RESPONSE = {'calendar.work': {'events': EV}}
