# the end as a duration of the time left: 50 minutes, reported 2 minutes ago, ends at 13:58 (*Appliance run*, *Entities*)
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/ap.py').read())
STATES[EN] = {'state': '50', 'attributes': {'device_class': 'duration', 'unit_of_measurement': 'min'}, 'last_updated': NOW - dt.timedelta(minutes=2)}
EXPECT = ['13:58']
EXPECT_SHARE = None
