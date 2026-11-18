# the widest labels: a freezer around -12.5
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/hg.py').read())
STATS_RESPONSE = {'statistics': {E: series(12, lambda x: -12.5 + 3.1 * math.exp(-((x - 0.5) / 0.1) ** 2))}}
STATES[E]['state'] = '-12.5'
