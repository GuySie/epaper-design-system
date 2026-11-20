# a sensor that reports a date and time in UTC: 23:30 UTC the day before is tomorrow, local time
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/bd.py').read())
STATES['sensor.bin_paper']['state'] = (NOW.replace(hour=23, minute=30) - dt.timedelta(hours=1)).astimezone(dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S+00:00')
STATES['sensor.bin_paper']['attributes']['device_class'] = 'timestamp'
