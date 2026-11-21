# a long title
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/rs.py').read())
INPUTS['header_title'] = 'The study on the first floor at the back'
EXPECT_BLOCK = False      # the hero block is the chip (*Glance with a word*, *Flagged*)
