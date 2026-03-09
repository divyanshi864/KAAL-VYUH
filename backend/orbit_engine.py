import pandas as pd
import random

def compute_positions(tle_list):

    records = []

    for sat in tle_list:
        records.append({
            "Satellite": sat["name"],
            "Latitude": random.uniform(-90, 90),
            "Longitude": random.uniform(-180, 180),
            "Altitude": random.uniform(300, 1500)
        })

    return pd.DataFrame(records)