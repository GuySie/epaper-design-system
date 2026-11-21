# busy on a grayscale panel
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/rs_busy.py').read())
MODELS = {'dev1': '3.5" GRAYSCALE_4'}
EXPECT_BLOCK = True      # the hero block is the chip (*Glance with a word*, *Flagged*)
