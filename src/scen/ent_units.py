import datetime as dt
TZ = dt.timezone(dt.timedelta(hours=1))
NOW = dt.datetime(2026, 8, 1, 20, 45, tzinfo=TZ)
SIZE = (384, 184)
# the units exactly as Home Assistant writes them (Greek mu, superscripts, the dot operator) and a few compatibility characters
ents = [('sensor.pm25', '4.2', 'μg/m³', 'PM2.5'), ('sensor.ec', '812', 'μS/cm', 'Conductivity'), ('sensor.irr', '412', 'W/m²', 'Irradiance'),
        ('sensor.flow', '1.4', 'm³/h', 'Ventilation'), ('sensor.par', '35', 'μmol/s⋅m²', 'PAR'), ('sensor.lat', '0.6', 'μs', 'Latency'),
        ('sensor.t', '21.4', '℃', 'Greenhouse'), ('sensor.area', '42', 'm²', 'Surface area'), ('sensor.r', '470', 'Ω', 'Resistance'),
        ('sensor.k', '0.25', 'm⁻¹', 'Extinction'), ('sensor.co2', '612', 'ppm', 'CO₂ office'), ('sensor.dp', '18', 'mmH₂O', 'Pressure difference')]
STATES = {e: {'state': s, 'attributes': {'unit_of_measurement': u}} for e, s, u, n in ents}
INPUTS = {f'entity_{i+1}': e for i, (e, *_r) in enumerate(ents)}
INPUTS.update({f'entity_{i+1}_label': n for i, (e, s, u, n) in enumerate(ents)})
INPUTS.update({f'entity_{i}': '' for i in range(len(ents)+1, 13)})
INPUTS['weekday_format'] = 'nl'
