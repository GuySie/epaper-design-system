exec(open(__import__('os').environ['EP_ROOT'] + '/scen/wx75_moon.py').read())
INPUTS = dict(INPUTS, displays=['d1'])
MODELS = {'d1': '4.3" MONO'}
