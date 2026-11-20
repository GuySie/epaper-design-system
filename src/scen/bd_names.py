# no words given: the sensors' names are the words
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/bd.py').read())
for n in range(1, 5): INPUTS['bin_%d_label' % n] = ''
