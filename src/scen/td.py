# To-do list: a shopping list with an overdue item, one due today, one due on Monday, and three done
import datetime as dt
TZ = dt.timezone(dt.timedelta(hours=1))
NOW = dt.datetime(2026, 8, 1, 14, 10, tzinfo=TZ)
E = 'todo.shopping'
def D(days): return (NOW + dt.timedelta(days=days)).strftime('%Y-%m-%d')
def items(open_, done): return [dict({'summary': s, 'uid': str(i), 'status': 'needs_action'}, **({'due': D(d)} if d is not None else {})) for i, (s, d) in enumerate(open_)] + [{'summary': s, 'uid': 'd' + str(i), 'status': 'completed'} for i, s in enumerate(done)]
OPEN = [('Oat milk', -1), ('Coffee beans', 0), ('Tomatoes', 2), ('Dish soap', None)]
DONE = ['Bread', 'Eggs', 'Olive oil']
TODO_RESPONSE = {E: {'items': items(OPEN, DONE)}}
STATES = {E: {'state': str(len(OPEN)), 'attributes': {'friendly_name': 'Shopping'}, 'last_updated': NOW - dt.timedelta(minutes=2)}}
DEVICE_NAMES = {E: 'Shopping'}
INPUTS = {'todo_entity': E, 'displays': ['dev1'], 'weekday_format': 'nl'}
