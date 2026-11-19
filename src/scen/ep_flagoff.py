exec(open(__import__('os').environ['EP_ROOT'] + '/scen/ep_sev.py').read())
# the switch off: no hour is flagged and the chart shows no thresholds
INPUTS['flag_price'] = False
