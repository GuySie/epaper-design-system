# another configuration: due days first
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/td_many.py').read())
INPUTS['due_first'] = True
