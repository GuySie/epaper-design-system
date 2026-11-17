# the 2-letter weekdays and 3-letter months (*Text rules* rule 8) in a language other than the default, on the calendar 4.26"
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/cal426.py').read())
INPUTS['weekday_format'] = 'pl'
