# high: the period reaches severe; the severe line sits close to the scale's top, whose label gives way
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/hg.py').read())
INPUTS.update({'flag_high': True, 'warning_high': 21.5, 'severe_high': 22.5})
