# every switch off (*Thresholds*): the readings of wx_warn, none of them flagged
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/wx_warn.py').read())
INPUTS.update({k: False for k in ('flag_temp_low', 'flag_temp_high', 'flag_wind_high', 'flag_rain_hour', 'flag_rain_day', 'flag_pollen_high')})
