"""Rain forecast on the 3.5": the rain chart with hourly bars, a day."""
from _rain import VARIABLES, payloads  # noqa: F401
PAYLOADS = payloads('rain-hourly', 3600, day_away=True)
