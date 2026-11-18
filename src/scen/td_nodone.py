# another configuration: the done items left out
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/td.py').read())
INPUTS['show_done'] = False
