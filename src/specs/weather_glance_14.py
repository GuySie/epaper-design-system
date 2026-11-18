# The Weather at a glance layout on the 1.4" screen: the same drawing as the 3.5" one (weather_glance_35.py) with the 200x200 tokens, so no
# drawing code of its own; only the kit's unit spacing differs.
exec(open(__import__('os').path.join(__import__('os').path.dirname(__file__), 'weather_glance_35.py')).read())
