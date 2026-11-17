exec(open(__import__('os').environ['EP_ROOT'] + '/scen/plants42.py').read())
INPUTS['displays']=['dev1']
MODELS={'dev1':'BWRY'}
