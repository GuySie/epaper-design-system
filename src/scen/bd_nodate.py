# the nearest bin's state is no date: it is left out
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/bd.py').read())
STATES['sensor.bin_paper']['state'] = 'soon'
