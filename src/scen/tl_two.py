# two entities
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/tl.py').read())
for i in range(3, 13):
    for k in ('', '_label', '_icon'): INPUTS.pop(f'entity_{i}{k}', None)
