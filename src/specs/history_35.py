"""History graph on the 3.5"."""
from _defaults import chart_points
from _history import PAYLOADS, WIDEST  # noqa: F401
# the most points the line shows on this screen; the page's data groups its readings to stay under it
POINTS = chart_points(__name__, WIDEST)
VARIABLES = {'hist_points': POINTS}
