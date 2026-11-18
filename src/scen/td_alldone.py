# every item done
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/td.py').read())
TODO_RESPONSE = {E: {'items': items([], DONE)}}
STATES[E]['state'] = '0'
