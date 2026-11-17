exec(open(__import__('os').environ['EP_ROOT'] + '/scen/plants42_y.py').read())
for i in range(9, 23): INPUTS[f'plant_{i}'] = ''
