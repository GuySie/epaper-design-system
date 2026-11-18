# a list without items: the empty statement
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/td.py').read())
TODO_RESPONSE = {E: {'items': []}}
STATES[E]['state'] = '0'
