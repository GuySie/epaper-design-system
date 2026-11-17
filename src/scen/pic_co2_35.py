# the reference picture of this layout (lib/pictures.py): its ordinary state, in English, on a BWRY panel
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/co2.py').read())
INPUTS['weekday_format'] = 'en'
INPUTS['displays'] = ['dev1']
MODELS = {'dev1': 'BWRY'}
# both levels at once: the afternoon crosses the warning line, then the severe line
def high(x):
    return 520 + 1150 * math.exp(-((x - 0.45) / 0.16) ** 2) + 300 * math.exp(-((x - 0.85) / 0.05) ** 2)
STATS_RESPONSE = {'statistics': {E: series(12, high)}}
STATES[E]['state'] = '1160'
