exec(open(__import__('os').environ['EP_ROOT'] + '/scen/rh_widest.py').read())
# the switch off: heavy rain is not flagged and the chart shows no thresholds
INPUTS['flag_rain_hour'] = False
