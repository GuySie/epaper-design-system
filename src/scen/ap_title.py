# a long title
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/ap.py').read())
EXPECT = []
INPUTS['header_title'] = 'Washing machine in the basement laundry room'
EXPECT_SHARE = None
