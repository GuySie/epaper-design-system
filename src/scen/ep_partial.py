exec(open(__import__('os').environ['EP_ROOT'] + '/scen/ep.py').read())
# the last hours of the day have no price: the statement stands in their part of the plot
NOW = at(9)
PRICE_RESPONSE = prices(CT[:14] + [None] * 10, NOW)
