exec(open(__import__('os').environ['EP_ROOT'] + '/scen/rain35.py').read())
STATES['sensor.neerslag_buienalarm_regen_data']['attributes']['data']['precip'] = [0] * len(codes)
