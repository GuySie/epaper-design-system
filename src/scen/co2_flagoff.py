# the switch off: a severe reading is not flagged and the chart shows no thresholds
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/co2_sev.py').read())
INPUTS['flag_co2'] = False
