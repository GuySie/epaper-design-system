# the 2-letter weekdays and 3-letter months (*Text rules* rule 8) in a language other than the default, on the next appointment 3.5"
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/appt35.py').read())
INPUTS['weekday_format'] = 'hr'
