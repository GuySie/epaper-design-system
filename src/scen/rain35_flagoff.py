# the switch off: a heavy shower is not flagged and the chart shows no thresholds
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/rain35_widest.py').read())
INPUTS['flag_rain_hour'] = False
