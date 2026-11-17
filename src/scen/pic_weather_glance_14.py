# the reference picture of this layout (lib/pictures.py): its ordinary state, in English, on a BWRY panel
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/wxp16.py').read())
INPUTS['weekday_format'] = 'en'
INPUTS['displays'] = ['dev1']
MODELS = {'dev1': 'BWRY'}
# both levels at once: a warning (wind, an hour of rain, a day of rain) and a severe state (pollen)
STATES['weather.home']['attributes']['wind_speed'] = 55
FORECASTS['weather.home']['hourly'][1]['precipitation'] = 3.2
STATES['sensor.kleenex_trees']['state'] = '160'
STATES['sensor.kleenex_trees']['attributes']['details'][0]['value'] = 160
