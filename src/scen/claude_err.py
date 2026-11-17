exec(open(__import__('os').environ['EP_ROOT'] + '/scen/claude35.py').read())
# the error view: no usage bar chosen
INPUTS.update({f'bar_{i}': '' for i in range(1, 5)})
