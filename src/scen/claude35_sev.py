exec(open(__import__('os').environ['EP_ROOT'] + '/scen/claude35.py').read())
STATES['sensor.w']['state']='100'
INPUTS['displays']=['dev1']
MODELS={'dev1':'BWRY'}
