import requests

def get_tle_data():
    url = "https://celestrak.org/NORAD/elements/active.txt"
    response = requests.get(url)
    lines = response.text.splitlines()

    tle_list = []
    for i in range(0, len(lines), 3):
        if i+2 < len(lines):
            tle_list.append({
                "name": lines[i],
                "line1": lines[i+1],
                "line2": lines[i+2]
            })
    return tle_list[:50]