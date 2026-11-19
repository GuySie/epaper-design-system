exec(open(__import__('os').environ['EP_ROOT'] + '/scen/ep.py').read())
# the widest footer (*Bar chart for prices*, Worst case): -10 ct now, the cheapest run ending at midnight, 12-hour time
CT = CT[:21] + [-10, 2, 4]
NOW = at(21)
PRICE_RESPONSE = prices(CT, NOW)
INPUTS.update({'time_format': '12h', 'weekday_format': 'en'})
