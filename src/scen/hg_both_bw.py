# both on, on a black/white panel: the low lines keep a paper notch inside a high fill
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/hg_both.py').read())
INPUTS['displays'] = ['d1']
MODELS = {'d1': 'X BW'}
