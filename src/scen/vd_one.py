# another configuration: one detail row
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/vd.py').read())
for k in ('detail_2', 'detail_3', 'detail_4'): INPUTS.pop(k)
