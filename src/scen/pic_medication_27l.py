# the reference picture of this layout (lib/pictures.py): its ordinary state, in English, on a BWRY panel
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/med29.py').read())
INPUTS['weekday_format'] = 'en'
INPUTS['displays'] = ['dev1']
MODELS = {'dev1': 'BWRY'}
# the page shows one level at a time: the severe one (40 hours since the last press)
INPUTS['button_entity'] = 'event.x'
STATES['event.x'] = {'state': (NOW - dt.timedelta(hours=40)).isoformat(), 'attributes': {'event_type': 'button_up'}}
