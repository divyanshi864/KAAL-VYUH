import os

EARTH_RADIUS = 6371
TLE_URL = "https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=2le"
MAX_OBJECTS = 75

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
