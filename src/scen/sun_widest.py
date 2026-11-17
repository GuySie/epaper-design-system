# the widest reading: the longest footer (Spanish, DURACIÓN DEL DÍA) and the widest 12-hour time, 10:44am / 10:44pm / 12:44am,
# in every column (the 24-hour form is narrower: no am/pm). Scenario clock UTC+1.
exec(open(__import__('os').environ['EP_ROOT'] + '/scen/sun35.py').read())
STATES['sun.sun']['attributes'].update(next_dawn='2026-02-01T23:44:00+00:00', next_rising='2026-02-02T09:44:00+00:00',
                                       next_noon='2026-02-02T09:44:00+00:00', next_setting='2026-02-01T21:44:00+00:00', next_dusk='2026-02-01T21:44:00+00:00')
INPUTS['weekday_format'] = 'es'
INPUTS['time_format'] = '12h'
