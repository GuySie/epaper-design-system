# the number at severe
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/vd.py').read())
STATS_RESPONSE = {'statistics': {E: series(24, lambda x: 950 + 880 * math.exp(-((x - 0.95) / 0.2) ** 2), 6)}}
STATES[E]['state'] = '1780'
INPUTS.update({'flag_high': True, 'warning_high': 1000, 'severe_high': 1500})
