import numpy as np

COLLISION_THRESHOLD_KM = 10

def detect_collisions(df):
    if df.empty:
        return []

    collisions = []
    satellites = df.to_dict(orient="records")

    for i in range(len(satellites)):
        for j in range(i + 1, len(satellites)):

            sat1 = satellites[i]
            sat2 = satellites[j]

            dx = sat1["X"] - sat2["X"]
            dy = sat1["Y"] - sat2["Y"]
            dz = sat1["Z"] - sat2["Z"]

            distance = np.sqrt(dx**2 + dy**2 + dz**2)

            if distance < COLLISION_THRESHOLD_KM:
                collisions.append({
                    "Satellite_1": sat1["Satellite"],
                    "Satellite_2": sat2["Satellite"],
                    "Distance_km": round(distance, 2)
                })

    return collisions
