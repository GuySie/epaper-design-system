exec(open(__import__('os').environ['EP_ROOT'] + '/scen/ep.py').read())
# an hour in the middle of the day has no price: its slot stays empty
PRICE_RESPONSE = prices(CT[:16] + [None] + CT[17:], NOW)
