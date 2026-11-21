# 12-hour time with a long programme: pm beside the hero, the programme cut, the percentage whole (*Appliance run*, *12-hour time*, *A long programme*)
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/ap.py').read())
INPUTS['time_format'] = '12h'
TRANSLATED[PG] = 'Cotton Eco 40-60 intensive with steam care'
EXPECT = ['2:32', 'pm', 'Cotton Eco', '...', '62']
EXPECT_SHARE = 62
