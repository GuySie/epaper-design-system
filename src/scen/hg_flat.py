# a nearly flat line: the smallest span keeps it from being stretched
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/hg.py').read())
STATS_RESPONSE = {'statistics': {E: series(12, lambda x: 21.3 + 0.1 * math.sin(x * 20), 0.05)}}
STATES[E]['state'] = '21.3'
