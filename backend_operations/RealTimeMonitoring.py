"""
Real-time Serial -> Routing Engine + Local API
- Reads JSON lines from ESP32 over serial
- Calls Google Directions API with alternatives=true
- Scores & selects optimal route based on sensors (rain, humidity, light)
- Recalculates when GPS moves significantly or when sensor triggers change
- Serves latest sensor/route info via local API
"""

import serial
import json
import time
import requests
import math
import sys
import threading
from flask import Flask, jsonify

# -------------------- DESTINATION FETCH --------------------
LOCAL_API_URL = "http://192.168.34.58:5000/gps/latest"
DESTINATION_REFRESH_INTERVAL = 5  # seconds

def fetch_destination_from_api():
    """
    Fetch destination coordinates from the local GPS API.
    Expected JSON structure:
    {
        "latitude": -26.1222561,
        "longitude": 28.0347158
    }
    """
    try:
        r = requests.get(LOCAL_API_URL, timeout=5)
        r.raise_for_status()
        data = r.json()
        lat = float(data.get("latitude", -26.1222561))
        lon = float(data.get("longitude", 28.0347158))
        print(f"[INFO] Destination refreshed from API: ({lat}, {lon})")
        return (lat, lon)
    except Exception as e:
        print(f"[WARN] Could not fetch destination from API: {e}")
        # fallback coordinates
        return (-26.1222561, 28.0347158)

# -------------------- CONFIG --------------------
SERIAL_PORT = "COM7"            # CHANGE to your ESP32 serial port
BAUD_RATE = 115200
GOOGLE_API_KEY = "AIzaSyCS5zg4O0jK68tfzibpSjx-0Ou1hXrcZ9A"   # CHANGE to your API key
DESTINATION = fetch_destination_from_api()      # (lat, lon) destination
HUMIDITY_THRESHOLD = 80      # percent -> treat as "likely rain"
LIGHT_THRESHOLD = 300        # lux -> low solar irradiance
MIN_RECALC_SECONDS = 10      # minimum seconds between route requests
MIN_MOVE_METERS = 25         # only force recalculation if moved > this (meters)
MAX_ALTERNATIVES = 3         # request alternatives=true -> Google returns some routes
REQUEST_TIMEOUT = 10         # seconds for HTTP calls

# -------------------- STATE --------------------
temperature = None
humidity = None
lux = None
rain = None        # 'WET' or 'DRY'
latitude = None
longitude = None

last_route_fetch_time = 0
last_origin = None
last_trigger_state = None
current_route = []   # list of human readable steps
estimated_time = None
route_status_label = "UNKNOWN"

# -------------------- UTIL --------------------
def haversine_meters(a, b):
    lat1, lon1 = a
    lat2, lon2 = b
    R = 6371000.0
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a_h = math.sin(dphi/2.0)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dl/2.0)**2
    return R * 2 * math.atan2(math.sqrt(a_h), math.sqrt(1-a_h))

def safe_json_loads(s):
    try:
        return json.loads(s)
    except json.JSONDecodeError:
        return None

def try_float(v, default=None):
    try:
        return float(v)
    except Exception:
        return default

# -------------------- SERIAL --------------------
def open_serial(port, baud):
    try:
        ser = serial.Serial(port, baud, timeout=2)
        time.sleep(1.0)
        print(f"[INFO] Opened serial port {port} @ {baud}")
        return ser
    except serial.SerialException as e:
        print(f"[ERROR] Could not open serial port {port}: {e}")
        sys.exit(1)

def read_esp32_line(ser):
    try:
        raw = ser.readline()
        if not raw:
            return None
        line = raw.decode("utf-8", errors="replace").strip()
        if not line:
            return None
        return safe_json_loads(line)
    except Exception as e:
        print(f"[ERROR] Serial read error: {e}")
        return None

# -------------------- GOOGLE DIRECTIONS --------------------
def fetch_routes(origin, destination):
    url = "https://maps.googleapis.com/maps/api/directions/json"
    params = {
        "origin": f"{origin[0]},{origin[1]}",
        "destination": f"{destination[0]},{destination[1]}",
        "alternatives": "true",
        "mode": "driving",
        "key": GOOGLE_API_KEY
    }
    try:
        r = requests.get(url, params=params, timeout=REQUEST_TIMEOUT)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"[ERROR] Google Directions request failed: {e}")
        return None

# -------------------- ROUTE SCORING --------------------
def score_and_pick_route(routes_json):
    global lux, rain, humidity
    if not routes_json or routes_json.get("status") != "OK":
        print("[WARN] No valid routes from Google")
        return None, None, None

    best_score = None
    best_route = None
    best_duration_text = None

    for route in routes_json.get("routes", [])[:MAX_ALTERNATIVES]:
        leg = route.get("legs", [])[0]
        duration_sec = leg.get("duration", {}).get("value", 0)
        steps = leg.get("steps", [])
        score = float(duration_sec)

        if rain == "WET":
            for step in steps:
                instr = step.get("html_instructions", "").lower()
                if any(word in instr for word in ("merge", "motorway", "freeway", "m1", "m2", "highway", "fwy", "ramp")):
                    score += 30

        if lux is not None and lux <= LIGHT_THRESHOLD:
            score += duration_sec * 0.10

        if humidity is not None and humidity >= HUMIDITY_THRESHOLD:
            score += 20

        if best_score is None or score < best_score:
            best_score = score
            best_route = route
            best_duration_text = leg.get("duration", {}).get("text", None)

    if not best_route:
        return None, None, None

    steps_list = []
    leg = best_route.get("legs", [])[0]
    for i, step in enumerate(leg.get("steps", []), start=1):
        instr = step.get("html_instructions", "").replace("<b>", "").replace("</b>", "")
        instr = instr.replace("<div style=\"font-size:0.9em\">", " ").replace("</div>", "")
        dist = step.get("distance", {}).get("text", "")
        dur = step.get("duration", {}).get("text", "")
        steps_list.append(f"Step {i}: {instr} ({dist}, {dur})")

    if rain == "WET":
        status_label = "OPTIMIZED for rain"
    elif humidity is not None and humidity >= HUMIDITY_THRESHOLD:
        status_label = "OPTIMIZED for high humidity"
    elif lux is not None and lux <= LIGHT_THRESHOLD:
        status_label = "OPTIMIZED for low solar irradiance"
    else:
        status_label = "NORMAL"

    return steps_list, best_duration_text, status_label

# -------------------- DISPLAY --------------------
def display_sensors_and_route():
    print("\n========== SENSOR READINGS ==========")
    print(f"Temperature     : {temperature if temperature is not None else 'N/A'} °C")
    print(f"Humidity        : {humidity if humidity is not None else 'N/A'} %")
    print(f"Light Intensity : {lux if lux is not None else 'N/A'} lux")
    print(f"Rain Sensor     : {rain if rain is not None else 'N/A'}")
    print(f"Current Location: {latitude if latitude is not None else 'N/A'}, {longitude if longitude is not None else 'N/A'}")
    print("=====================================")
    print("[INFO] Access local API at http://<PC_IP>:5000/api/sensors\n")

def display_route(steps, eta, status):
    print(f"--- Optimal Route --- ({status})")
    if steps:
        for s in steps:
            print(s)
    else:
        print("No route steps available.")
    if eta:
        print(f"Estimated Time: {eta}")
    print("==================================================\n")

# -------------------- LOCAL API --------------------
app = Flask(__name__)

def API_sensors_and_route():
    global temperature, humidity, lux, rain, latitude, longitude
    global current_route, estimated_time, route_status_label

    return {
        "sensors": {
            "temperature": temperature if temperature is not None else "N/A",
            "humidity": humidity if humidity is not None else "N/A",
            "light": lux if lux is not None else "N/A",
            "rain": rain if rain is not None else "N/A",
            "latitude": latitude if latitude is not None else "N/A",
            "longitude": longitude if longitude is not None else "N/A"
        },
        "route": {
            "status": route_status_label,
            "estimated_time": estimated_time if estimated_time else "N/A",
            "steps": current_route if current_route else []
        }
    }

@app.route("/api/sensors", methods=["GET"])
def get_sensors():
    return jsonify(API_sensors_and_route())

@app.route("/api/directions", methods=["GET"])
def get_directions():
    """
    Returns the current route directions only.
    """
    return jsonify({
        "status": route_status_label,
        "estimated_time": estimated_time if estimated_time else "N/A",
        "steps": current_route if current_route else []
    })

def start_local_api(host="0.0.0.0", port=5000):
    print(f"[INFO] Starting local API on http://{host}:{port}/api/sensors")
    app.run(host=host, port=port, debug=False, use_reloader=False)

def destination_updater():
    global DESTINATION
    while True:
        DESTINATION = fetch_destination_from_api()
        time.sleep(DESTINATION_REFRESH_INTERVAL)

# -------------------- MAIN LOOP --------------------
def main_loop():
    global temperature, humidity, lux, rain, latitude, longitude
    global last_route_fetch_time, last_origin, last_trigger_state, current_route, estimated_time, route_status_label

    ser = open_serial(SERIAL_PORT, BAUD_RATE)

    try:
        while True:
            data = read_esp32_line(ser)
            if data:
                temperature = try_float(data.get("temperature"))
                humidity = try_float(data.get("humidity"))
                lux = try_float(data.get("lux"))
                rain = "WET" if int(data.get("rain", 0)) == 1 else "DRY"
                latitude = try_float(data.get("latitude"), default=-26.2041059)
                longitude = try_float(data.get("longitude"), default=28.0473197)

                display_sensors_and_route()

                triggers = (
                    rain == "WET",
                    (humidity is not None and humidity >= HUMIDITY_THRESHOLD),
                    (lux is not None and lux <= LIGHT_THRESHOLD)
                )
                origin = (latitude, longitude)
                now = time.time()

                moved = False
                if last_origin is None or haversine_meters(origin, last_origin) >= MIN_MOVE_METERS:
                    moved = True

                triggers_changed = (triggers != last_trigger_state)
                time_ok = (now - last_route_fetch_time) >= MIN_RECALC_SECONDS

                if (moved or triggers_changed) and time_ok:
                    print("[INFO] Fetching route alternatives from Google...")
                    routes_json = fetch_routes(DESTINATION, origin)
                    last_route_fetch_time = now
                    last_origin = origin
                    last_trigger_state = triggers

                    steps, eta, status = score_and_pick_route(routes_json)
                    current_route = steps or []
                    estimated_time = eta
                    route_status_label = status or "UNKNOWN"
                    display_route(current_route, estimated_time, route_status_label)
                else:
                    display_route(current_route, estimated_time, route_status_label)

            time.sleep(1.0)

    except KeyboardInterrupt:
        print("\n[INFO] Exiting...")

    finally:
        try:
            ser.close()
            print("[INFO] Serial closed.")
        except:
            pass

# -------------------- ENTRY POINT --------------------
if __name__ == "__main__":
    if GOOGLE_API_KEY == "AIzaSyCS5zg4O0jK68tfzibpSjx-0Ou1hXrcZ9A":
        print("[WARNING] Please set your GOOGLE_API_KEY in the script before running.")

    # Start local API
    threading.Thread(target=start_local_api, daemon=True).start()

    # Start background destination refresher
    threading.Thread(target=destination_updater, daemon=True).start()

    print("Starting routing engine. Press Ctrl+C to stop.")
    main_loop()

