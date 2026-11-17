# the overdue switch off: 40 hours after the last press, the date stays plain
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/med_sev.py').read())
INPUTS['flag_late'] = False
