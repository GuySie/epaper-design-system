# low: a row at severe and one at warning (the battery at 12 %, humidity at 24 %)
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/lv.py').read())
STATES['sensor.battery']['state'] = '12'
STATES['sensor.humidity']['state'] = '24'
INPUTS.update({'flag_low': True, 'warning_low': 30, 'severe_low': 15})
