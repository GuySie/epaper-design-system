exec(open(__import__('os').environ['EP_ROOT'] + '/scen/ep.py').read())
# the last hour of the day: fewer hours left than the cheapest run, the footer has no right side
NOW = at(23)
