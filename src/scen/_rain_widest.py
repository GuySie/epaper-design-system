# the widest reading: the heaviest bar at the top of the scale (50 mm/h), severe across most of the two hours, and the
# longest footer (Spanish, 24-hour times: LLUVIA FUERTE ... PICO 50)
MM = [0, 3, 12, 15, 20, 25, 30, 35, 40, 45, 50, 50, 45, 40, 35, 30, 25, 20, 15, 12, 11, 10.5, 10, 6, 3, 1]
codes = [0 if m <= 0 else round(109 + 32 * math.log10(m)) for m in MM]
codes = [c + 1 if m == 50 else c for c, m in zip(codes, MM)]   # the sensor's code for 50 rounds down to 48.7: the next code up reads 50 or more
STATES['sensor.neerslag_buienalarm_regen_data']['attributes']['data']['precip'] = codes
INPUTS['weekday_format'] = 'es'
INPUTS['time_format'] = '24h'
