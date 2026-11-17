# a shower past the warning line (2.5 mm/h) that stays under severe (10 mm/h): warning is a reference only, so no bar is coloured
MM = [0, 0, 0, 0, 0.3, 0.8, 1.5, 2.6, 4, 6, 7, 5, 3, 2, 1, 0.5, 0.3, 0.2, 0.1, 0, 0, 0, 0, 0, 0, 0]
codes = [0 if m <= 0 else round(109 + 32 * math.log10(m)) for m in MM]
STATES['sensor.neerslag_buienalarm_regen_data']['attributes']['data']['precip'] = codes
