# a blueprint from another release than the templates: the title row and the error block with both ids
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/wxp16.py').read())
INPUTS['weekday_format'] = 'en'
OVERRIDE = {'ds_set': 'a1b2c3'}
MASK_SET = '7F3E9D'
