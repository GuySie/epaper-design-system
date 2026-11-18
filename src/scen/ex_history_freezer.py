# an example of what the page is used for (README, lib/pictures.py): in English, on a BWRY panel
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/hg.py').read())
STATS_RESPONSE = {'statistics': {E: series(24, lambda x: -18.6 + 0.5 * math.sin(x * 60) + 5.5 * math.exp(-((x - 0.7) / 0.04) ** 2), 0.2)}}
STATES[E]['state'] = '-18.4'
STATES[E]['attributes'].update(friendly_name='Freezer')
DEVICE_NAMES[E] = 'Freezer'
INPUTS.update({'hours': '24', 'flag_high': True, 'warning_high': -15, 'severe_high': -12})
INPUTS.update({'weekday_format': 'en', 'displays': ['dev1']})
MODELS = {'dev1': 'BWRY'}
