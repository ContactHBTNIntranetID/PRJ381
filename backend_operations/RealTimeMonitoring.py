import serial
import json
import time
import requests

# --------------------------
# CONFIGURATION
# --------------------------
SERIAL_PORT = "COM7"         # ESP32 Serial port
BAUD_RATE = 115200
GOOGLE_MAPS_API_KEY = "AIzaSyCS5zg4O0jK68tfzibpSjx-0Ou1hXrcZ9A"
HUMIDITY_THRESHOLD = 80       # % RH
LIGHT_THRESHOLD = 300         # lux

# --------------------------
# VARIABLES
# --------------------------
temperature = None
humidity = None
lux = None
rain = None
latitude = None
longitude = None
current_route = []
estimated_time = None

# --------------------------
# HELPER FUNCTIONS
# --------------------------

def read_esp32_data():
    """Read one line of JSON data from ESP32."""
    global temperature, humidity, lux, rain, latitude, longitude
    try:
        with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=2) as ser:
            line = ser.readline().decode('utf-8').strip()
            if not line:
                return False
            data = json.loads(line)
            temperature = data.get("temperature", 0.0)
            humidity = data.get("humidity", 0.0)
            lux = data.get("lux", 0.0)
            rain = "WET" if data.get("rain", 0) else "DRY"
            latitude = data.get("latitude", -26.2041059)
            longitude = data.get("longitude", 28.0473197)
            return True
    except (serial.SerialException, json.JSONDecodeError) as e:
        print(f"[ERROR] Serial read error: {e}")
        return False

def display_sensor_data():
    """Nicely print sensor readings."""
    print("\n================= SENSOR READINGS =================")
    print(f"Temperature: {temperature:.1f} °C")
    print(f"Humidity: {humidity:.1f} %")
    print(f"Light Intensity: {lux:.1f} lux")
    print(f"Rain Sensor: {rain}")
    print(f"Current Location: {latitude:.6f}, {longitude:.6f}")
    print("==================================================\n")

def check_thresholds():
    """Check if reroute is required."""
    if rain == "WET":
        return True, "Rain detected"
    if humidity >= HUMIDITY_THRESHOLD:
        return True, "High humidity detected"
    if lux <= LIGHT_THRESHOLD:
        return True, "Low solar irradiance detected"
    return False, ""

def fetch_optimal_route(origin, destination):
    """Fetch route from Google Maps API."""
    url = "https://maps.googleapis.com/maps/api/directions/json"
    params = {
        "origin": f"{origin[0]},{origin[1]}",
        "destination": f"{destination[0]},{destination[1]}",
        "key": GOOGLE_MAPS_API_KEY,
        "mode": "driving"
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"[ERROR] Google Maps API request failed: {e}")
        return None

def parse_route(data):
    """Extract steps and estimated time from route data."""
    global current_route, estimated_time
    current_route.clear()
    if data.get("status") != "OK" or not data.get("routes"):
        print("[ERROR] No route found")
        return
    leg = data["routes"][0]["legs"][0]
    estimated_time = leg["duration"]["text"]
    steps = leg.get("steps", [])
    for i, step in enumerate(steps, start=1):
        instruction = step["html_instructions"].replace("<b>", "").replace("</b>", "")
        instruction = instruction.replace("<div style=\"font-size:0.9em\">", " ").replace("</div>", "")
        distance = step["distance"]["text"]
        duration = step["duration"]["text"]
        current_route.append(f"Step {i}: {instruction} ({distance}, {duration})")

def display_route(status_msg="Route Status: NORMAL"):
    """Print the route nicely."""
    print(f"--- Optimal Route --- ({status_msg})")
    for step in current_route:
        print(step)
    if estimated_time:
        print(f"Estimated Time: {estimated_time}")
    print("==================================================\n")

# --------------------------
# MAIN LOOP
# --------------------------
def main():
    destination = (-26.1222561, 28.0347158)  # Example destination

    while True:
        if read_esp32_data():
            display_sensor_data()
            
            reroute_needed, reason = check_thresholds()
            route_status_msg = f"OPTIMIZED for {reason.lower()}" if reroute_needed else "NORMAL"
            
            route_data = fetch_optimal_route((latitude, longitude), destination)
            if route_data:
                parse_route(route_data)
                display_route(route_status_msg)
        
        time.sleep(5)

if __name__ == "__main__":
    main()
