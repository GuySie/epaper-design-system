exec(open(__import__('os').environ['EP_ROOT'] + '/scen/wx75neg.py').read())
INPUTS = dict(INPUTS, displays=['d1'])
MODELS = {'d1': '4.3" MONO'}
