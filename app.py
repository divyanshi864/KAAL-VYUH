from flask import Flask, render_template, request, jsonify
import pandas as pd
from backend.data_fetcher import get_tle_data
from backend.orbit_engine import compute_positions
from backend.risk_engine import classify_risk
from skyfield.api import EarthSatellite, load
from flask import jsonify
import requests
from datetime import datetime
app = Flask(__name__)

@app.route("/real_satellites")
def real_satellites():

    url = "https://celestrak.org/NORAD/elements/stations.txt"
    tle_data = requests.get(url).text.splitlines()

    ts = load.timescale()
    t = ts.now()

    satellites = []

    for i in range(0, len(tle_data), 3):
        name = tle_data[i].strip()
        line1 = tle_data[i+1].strip()
        line2 = tle_data[i+2].strip()

        sat = EarthSatellite(line1, line2, name, ts)
        geocentric = sat.at(t)
        position = geocentric.position.km

        satellites.append({
            "name": name,
            "x": position[0] / 1000,
            "y": position[1] / 1000,
            "z": position[2] / 1000
        })

    return jsonify(satellites)



def get_data():
    tle_data = get_tle_data()
    df = compute_positions(tle_data)
    df = classify_risk(df)
    return df

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    df = get_data()

    high = len(df[df["Risk"] == "High"])
    medium = len(df[df["Risk"] == "Medium"])
    low = len(df[df["Risk"] == "Low"])

    coords = df[["Latitude", "Longitude", "Risk"]].values.tolist()

    return render_template("dashboard.html",
                           high=high,
                           medium=medium,
                           low=low,
                           coords=coords)

@app.route("/heatmap")
def heatmap():
    df = get_data()

    print("DF LENGTH:", len(df))

    coords = df[["Latitude", "Longitude"]].dropna().values.tolist()

    print("COORDS LENGTH:", len(coords))

    return render_template("heatmap.html", coords=coords)

@app.route("/chatbot")
def chatbot():
    return render_template("chatbot.html")

@app.route("/chat", methods=["POST"])
def chat():
    msg = request.json["message"].lower()

    if "collision" in msg:
        reply = "Collisions occur when satellites approach below safe distance thresholds."
    elif "risk" in msg:
        reply = "Risk levels are determined by altitude and orbital congestion."
    elif "heatmap" in msg:
        reply = "Heatmap shows global orbital density distribution."
    else:
        reply = "I am your Orbital Intelligence Assistant."

    return jsonify({"reply": reply})

@app.route("/visualization")
def visualization():
    df = get_data()
    coords = df[["Latitude", "Longitude", "Risk"]].values.tolist()
    return render_template("visualization.html", coords=coords)

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)