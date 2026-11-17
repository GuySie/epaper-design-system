exec(open(__import__('os').environ['EP_ROOT'] + '/scen/wx75p.py').read())
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/_calendar.py').read())
NOW = CAL_NOW                      # 10:20: the 10:00 meeting is running
