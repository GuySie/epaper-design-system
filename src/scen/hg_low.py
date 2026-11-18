# low: the morning dips under both low values
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/hg.py').read())
INPUTS.update({'flag_low': True, 'warning_low': 19.5, 'severe_low': 18.8})
