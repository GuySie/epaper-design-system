# The 4.1" calendar's layout on the Seeed 4.26" kit (800 x 480, 92.8 x 55.68 mm): the same token-driven
# drawing, with the 800x480-0.12 tokens (TRMNL21 throughout, 2 px lines), so no drawing code of its own.
exec(open(__import__('os').path.join(__import__('os').path.dirname(__file__), 'calendar_41.py')).read())
