from backend.data_fetcher import fetch_tle_data
from backend.orbit_engine import propagate_orbits
from backend.risk_engine import calculate_risk
from backend.collision_engine import detect_collisions

_cached_data = None
_cached_collisions = None

def load_system_data():
    global _cached_data, _cached_collisions

    tle = fetch_tle_data()
    df = propagate_orbits(tle)
    df = calculate_risk(df)
    collisions = detect_collisions(df)

    _cached_data = df
    _cached_collisions = collisions

def get_data():
    global _cached_data
    if _cached_data is None:
        load_system_data()
    return _cached_data

def get_collisions():
    global _cached_collisions
    if _cached_collisions is None:
        load_system_data()
    return _cached_collisions
