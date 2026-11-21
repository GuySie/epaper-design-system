# a state in both lists: severe wins
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/rs.py').read())
INPUTS.update({'warning_states': ['Free'], 'severe_states': ['free']})
EXPECT_BLOCK = True      # the hero block is the chip (*Glance with a word*, *Flagged*)
EXPECT_FILL = 'red'      # severe wins: the block's fill is severe's, red on this panel
