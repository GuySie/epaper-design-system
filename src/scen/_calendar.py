# the calendar's data on a weather scenario: a calendar scenario's calendar, events and inputs (CALENDAR_FROM, default cal42),
# drawn on the 7.5" portrait. The weather's time, panel and inputs win; CAL_NOW is the calendar scenario's time.
import os
_w, _wi, _now, _m = dict(STATES), dict(INPUTS), NOW, globals().get('MODELS')
exec(open(os.environ['EP_ROOT'] + f"/scen/{globals().get('CALENDAR_FROM', 'cal42')}.py").read())
CAL_NOW = NOW
STATES, INPUTS, NOW = {**STATES, **_w}, {**INPUTS, **_wi}, _now
if _m:
    MODELS = _m
SIZE = (480, 800)
