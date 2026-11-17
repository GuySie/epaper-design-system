exec(open(__import__('os').environ['EP_ROOT'] + '/scen/wxp16.py').read())
INPUTS.update({'warning_rain_hour': 0.5, 'warning_wind_high': 15, 'warning_temp_high': 11, 'warning_rain_day': 3, 'warning_pollen_high': 90, 'severe_pollen_high': 150, 'wind_or_precipitation': 'windspeed'})
MODELS = {}
