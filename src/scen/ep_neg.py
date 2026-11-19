exec(open(__import__('os').environ['EP_ROOT'] + '/scen/ep.py').read())
# a sunny day: negative prices at midday
CT = [9, 8, 7, 7, 7, 8, 10, 12, 10, 5, 1, -2, -4, -3, 0, 5, 9, 13, 16, 14, 12, 10, 9, 9]
NOW = at(9)
PRICE_RESPONSE = prices(CT, NOW)
