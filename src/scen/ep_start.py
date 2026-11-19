exec(open(__import__('os').environ['EP_ROOT'] + '/scen/ep.py').read())
# the first hour of the day: no hour is gone
NOW = at(0)
