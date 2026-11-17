exec(open(__import__('os').environ['EP_ROOT'] + '/scen/co2.py').read())
def mid(x):
    return 500 + 700 * math.exp(-((x - 0.6) / 0.15) ** 2)
STATS_RESPONSE = {'statistics': {E: series(24, mid)}}
STATES[E]['state'] = '640'
INPUTS.update({'hours': '24', 'weekday_format': 'en', 'time_format': '12h'})
MODELS = {'dev1': 'Solum 3.5 BWRY'}
