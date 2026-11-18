# another configuration: no detail rows and no icon
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/vd.py').read())
for k in ('detail_1', 'detail_2', 'detail_3', 'detail_4', 'icon'): INPUTS.pop(k)
