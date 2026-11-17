# The 7.5" weather layout on the Seeed 4.26" kit (800 x 480, 92.8 x 55.68 mm): the same pixels, so the same drawing with the
# 800x480-0.12 tokens (2 px lines, Bold where TRMNL21 Regular stems are under 0.25 mm), no drawing code of its own.
exec(open(__import__('os').path.join(__import__('os').path.dirname(__file__), 'weather_75.py')).read())
