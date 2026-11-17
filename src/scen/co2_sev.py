exec(open(__import__('os').environ['EP_ROOT'] + '/scen/co2.py').read())
def high(x):
    return 520 + 1150 * math.exp(-((x - 0.45) / 0.16) ** 2) + 300 * math.exp(-((x - 0.85) / 0.05) ** 2)
STATS_RESPONSE = {'statistics': {E: series(12, high, skip=range(20, 26))}}
STATES[E]['state'] = '1160'
