# no progress sensor: the bar follows the time, no percentage is written (*Appliance run*, *Running*)
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/ap.py').read())
INPUTS['progress_entity'] = ''
EXPECT = ['Eco 40']
EXPECT_SHARE = 49    # 80 of the 162 minutes since the status last changed
EXPECT_NOT = ['%']
