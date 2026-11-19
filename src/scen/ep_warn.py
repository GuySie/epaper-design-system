exec(open(__import__('os').environ['EP_ROOT'] + '/scen/ep.py').read())
# the current hour is at the warning level: the footer is a warning chip
NOW = at(17)
