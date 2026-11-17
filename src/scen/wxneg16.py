exec(open(__import__('os').environ['EP_ROOT'] + '/scen/wx.py').read())
SIZE=(200,200)
STATES['weather.home']['attributes']['temperature']=-12.4
