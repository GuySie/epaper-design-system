exec(open(__import__('os').environ['EP_ROOT'] + '/scen/entities35.py').read())
_k=[k for k in INPUTS if k.startswith('entity_') and not k.endswith('label') and INPUTS[k]]
for k in _k[:len(_k)//2+1]: STATES[INPUTS[k]]['state']='unavailable'
