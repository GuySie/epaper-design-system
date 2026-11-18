# high: one row at warning (the battery at 82 % of full, warning from 80 %)
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/lv.py').read())
INPUTS.update({'flag_high': True, 'warning_high': 80, 'severe_high': 90})
