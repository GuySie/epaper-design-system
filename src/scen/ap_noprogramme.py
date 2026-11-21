# no programme: the percentage alone
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/ap.py').read())
INPUTS['programme_entity'] = ''
EXPECT = ['62']
EXPECT_NOT = ['Eco', '·']
EXPECT_SHARE = None
