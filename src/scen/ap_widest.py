# the widest reading, 20:00: the icon steps down, the number never shrinks (*Glance*, *Too wide*)
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/ap.py').read())
STATES[EN]['state'] = NOW.replace(hour=20, minute=0).isoformat()
EXPECT = ['20:00']
EXPECT_SHARE = 62
