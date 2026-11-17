exec(open(__import__('os').environ['EP_ROOT'] + '/scen/wx75p_warn.py').read())
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/_calendar.py').read())
INPUTS['displays'] = ['dev1']
MODELS = {'dev1': 'BWRY'}
