exec(open(__import__('os').environ['EP_ROOT'] + '/scen/openings_1.py').read())
STATES['binary_sensor.living_room_balcony_door']['state']='on'
INPUTS['weekday_format']='en'
