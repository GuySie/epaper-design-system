import datetime as dt
TZ = dt.timezone(dt.timedelta(hours=1))
NOW = dt.datetime(2026, 2, 1, 14, 10, tzinfo=TZ)
STATES = {
 'sun.sun': {'state': 'above_horizon', 'attributes': {'azimuth': 210.0, 'elevation': 14.5,
   'next_dawn': '2026-02-02T06:38:00+00:00', 'next_rising': '2026-02-02T07:12:00+00:00', 'next_noon': '2026-02-02T11:28:00+00:00',
   'next_setting': '2026-02-01T15:52:00+00:00', 'next_dusk': '2026-02-01T16:27:00+00:00'}},
 'sensor.moon_phase': {'state': 'waxing_crescent', 'attributes': {}, 'integration': 'moon'},
 'sensor.moon_az': {'state': '140'}, 'sensor.moon_alt': {'state': '22'},
}
INPUTS = {'weekday_format': 'nl', 'moon_azimuth_sensor': 'sensor.moon_az', 'moon_altitude_sensor': 'sensor.moon_alt'}
STATES['zone.home'] = {'state': '0', 'attributes': {'latitude': 52.37, 'longitude': 4.90}}
