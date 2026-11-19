exec(open(__import__('os').environ['EP_ROOT'] + '/scen/ep.py').read())
# a price above the top of the scale is clipped at the edge
CT = CT[:18] + [45] + CT[19:]
PRICE_RESPONSE = prices(CT, NOW)
