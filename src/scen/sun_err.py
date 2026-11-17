exec(open(__import__('os').environ['EP_ROOT'] + '/scen/sun35.py').read())
# the error view: the sun integration is missing
STATES.pop('sun.sun', None)
