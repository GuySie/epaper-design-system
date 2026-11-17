import datetime as dt
TZ = dt.timezone(dt.timedelta(hours=1))
NOW = dt.datetime(2026, 8, 2, 21, 56, tzinfo=TZ)
P = [('Alocasia', 27), ('Araucaria', 21), ('Begonia 0785', 28), ('Begonia B4B0', 24), ('Begonia D4E0', 31), ('Begonia maculata', 25), ('Sansevieria', 33),
     ('Aeschynanthus', 32), ('Phlebodium', 18), ('Phlebo davana', 26), ('Scindapsus', 29), ('Spathiphyllum', 36), ('Strelitzia', 38), ('Zamioculcas', 26),
     ('Alocasia zebrina', 25), ('Marguerite', 0), ('Mandevilla', 22), ('Campanula', 55), ('Lavandula', 26), ('Monstera', 31)]
STATES = {f'sensor.p{i}': {'state': str(v), 'attributes': {'friendly_name': f'{n} Soil moisture', 'unit_of_measurement': '%'}} for i, (n, v) in enumerate(P)}
INPUTS = {f'plant_{i+1}': f'sensor.p{i}' for i in range(len(P))}
INPUTS.update({f'plant_{i+1}_label': '' for i in range(22)})
INPUTS.update({f'plant_{i+1}': '' for i in range(len(P), 22)})
INPUTS.update({'weekday_format': 'nl', 'header_title': 'Plant water', 'severe_moisture_low': 14})
