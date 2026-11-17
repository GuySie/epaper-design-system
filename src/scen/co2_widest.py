# the widest reading (registry: 4000): the concentration climbs to 4000 ppm and is there now, so the current value and the peak are both 4000
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/co2.py').read())
def climb(x):
    return 480 + 3520 * x ** 3
STATS_RESPONSE = {'statistics': {E: series(12, climb)}}
STATES[E]['state'] = '4000'
