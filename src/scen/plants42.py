import datetime as dt
TZ = dt.timezone(dt.timedelta(hours=1))
NOW = dt.datetime(2026, 8, 1, 20, 45, tzinfo=TZ)
P = [('Basil', 9), ('Calathea', 14), ('Pilea', 21), ('Fern', 24), ('Monstera', 31), ('Ficus', 34), ('Kentia', 36),
     ('Sansevieria trifasciata', 38), ('Aloe vera', 39), ('Zamioculcas', 41), ('Hoya', 'unavailable'), ('Peperomia', 44), ('Olive tree', 45),
     ('Strelitzia', 47), ('Alocasia', 48), ('Pothos', 50), ('Philodendron', 52), ('Lemon tree', 53), ('Coffee plant', 55),
     ('Yucca', 57), ('Dracaena', 60), ('Areca', 62)]
STATES = {f'sensor.p{i}': {'state': str(v), 'attributes': {'friendly_name': f'{n} Soil moisture', 'unit_of_measurement': '%'}} for i, (n, v) in enumerate(P)}
INPUTS = {f'plant_{i+1}': f'sensor.p{i}' for i in range(len(P))}
INPUTS.update({f'plant_{i+1}_label': '' for i in range(22)})
INPUTS['weekday_format'] = 'nl'
