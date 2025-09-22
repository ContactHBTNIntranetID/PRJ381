import requests
import numpy as np
from datetime import datetime, timedelta
from pymongo import MongoClient
from statsmodels.tsa.arima.model import ARIMA
import time
import sys
import io

# Ensure UTF-8 stdout (optional, avoids encoding errors)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# ---------------- CONFIG ----------------
OWM_API_KEY = "bb77e1d47d0f3700b1a27f6613c07b9b"
GOOGLE_MAPS_API_KEY = "AIzaSyCS5zg4O0jK68tfzibpSjx-0Ou1hXrcZ9A"

SOLAR_THRESHOLD = 800  # W/m²
RAIN_THRESHOLD = 1     # mm
LOW_SOLAR_DURATION = 30  # minutes
FORECAST_MINUTES_AHEAD = 15  # How far ahead to forecast

CURRENT_LOCATION = {"lat": -25.746111, "lon": 28.188056}
DESTINATION = {"lat": -25.9600, "lon": 28.1500}

from Connections import return_documents

# ---------------- WEATHER FUNCTIONS ----------------
def fetch_live_weather(lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OWM_API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code != 200:
        print("Error fetching weather data")
        return None, None
    data = response.json()
    cloudiness = data.get("clouds", {}).get("all", 0)
    solar_irradiance = 1000 * (1 - cloudiness / 100)
    rain = data.get("rain", {}).get("1h", 0)
    return solar_irradiance, rain

# ---------------- GOOGLE MAPS ROUTING ----------------
def fetch_routes(start, end):
    url = "https://maps.googleapis.com/maps/api/directions/json"
    params = {
        "origin": f"{start['lat']},{start['lon']}",
        "destination": f"{end['lat']},{end['lon']}",
        "alternatives": "true",
        "key": GOOGLE_MAPS_API_KEY
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print("Error fetching routes from Google Maps")
        return []
    data = response.json()
    return data.get("routes", [])

# ---------------- PREDICTIVE SCORING ----------------
def forecast_weather(documents, minutes_ahead=FORECAST_MINUTES_AHEAD):
    if not documents:
        return None, None, 0, 0

    solar = np.array([doc['solar_irradiance_wm2'] for doc in documents])
    rain = np.array([doc['rainfall_mm'] for doc in documents])

    # Fit ARIMA models
    try:
        model_solar = ARIMA(solar, order=(1,1,1)).fit()
        model_rain = ARIMA(rain, order=(1,1,1)).fit()
    except Exception as e:
        print(f"ARIMA fitting error: {e}")
        return None, None, 0, 0

    # Forecast next minutes
    forecast_solar = model_solar.forecast(steps=minutes_ahead)
    forecast_rain = model_rain.forecast(steps=minutes_ahead)

    # In-sample one-step forecast for accuracy
    in_sample_solar = model_solar.predict(start=1, end=len(solar)-1)

    # Avoid division by zero
    epsilon = 1e-5
    mape_solar = np.mean(np.abs((solar[1:] - in_sample_solar) / (solar[1:] + epsilon))) * 100
    solar_accuracy = max(0, min(100, 100 - mape_solar))

    # Handle low-variance or minimal rain data to avoid 0% accuracy
    if np.max(rain) < 0.1 or len(rain) < 5:
        rain_accuracy = 100
    else:
        in_sample_rain = model_rain.predict(start=1, end=len(rain)-1)
        mape_rain = np.mean(np.abs((rain[1:] - in_sample_rain) / (rain[1:] + epsilon))) * 100
        rain_accuracy = max(0, min(100, 100 - mape_rain))

    return forecast_solar, forecast_rain, solar_accuracy, rain_accuracy

ACCURACY_THRESHOLD = 70  # percent

def score_route_with_forecast(route, collection_name):
    documents = return_documents(collection_name)
    if not documents:
        return 0, 0, 0, 0, 0

    forecast_solar, forecast_rain, solar_acc, rain_acc = forecast_weather(documents)

    if forecast_solar is None or forecast_rain is None:
        return 0, 0, 0, 0, 0

    # Combine forecast + live weather
    live_solar, live_rain = fetch_live_weather(CURRENT_LOCATION['lat'], CURRENT_LOCATION['lon'])
    forecast_solar = np.append(forecast_solar, live_solar)
    forecast_rain = np.append(forecast_rain, live_rain)

    avg_solar = np.mean(forecast_solar)
    avg_rain = np.mean(forecast_rain)
    score = avg_solar - (avg_rain * 100)

    return score, avg_solar, avg_rain, solar_acc, rain_acc

# ---------------- PRETTY PRINT FUNCTIONS ----------------
def print_route_details(route, solar, rain, solar_acc, rain_acc):
    print(f"\n\033[1;34mBest route:\033[0m Solar={solar:.1f}, Rain={rain:.2f}, "
          f"SolarAcc={solar_acc:.1f}%, RainAcc={rain_acc:.1f}%")

    for leg in route['legs']:
        total_distance = leg['distance']['text']
        total_duration = leg['duration']['text']
        print(f"\n\033[1;32mInitial Best Route:\033[0m")
        print(f"\033[1;33mOverall Distance: {total_distance} | Travel Time: {total_duration}\033[0m\n")

        for step in leg['steps']:
            instruction = step['html_instructions'] if isinstance(step, dict) else step
            step_distance = step.get('distance', {}).get('text', 'N/A') if isinstance(step, dict) else "N/A"
            step_duration = step.get('duration', {}).get('text', 'N/A') if isinstance(step, dict) else "N/A"

            print(f"➡️  {instruction}")
            print(f"   📏 Distance: {step_distance} | ⏱ Time: {step_duration}\n")

        print(f"✅ \033[1;35mLeg Summary:\033[0m {total_distance}, {total_duration}\n")



# ---------------- MAIN ROUTE SELECTION ----------------
def select_best_route(start, end, collection_name):
    routes = fetch_routes(start, end)
    if not routes:
        print("No routes from Google Maps, picking route by predicted weather conditions...")
        fake_route = {"legs": [{"steps": ["Direct route"]}]}
        score, solar, rain, solar_acc, rain_acc = score_route_with_forecast(fake_route, collection_name)
        print(f"Selected route: Solar={solar:.1f}, Rain={rain:.2f}, SolarAcc={solar_acc:.1f}%, RainAcc={rain_acc:.1f}%")
        return fake_route

    best_route = None
    best_score = -float("inf")
    for route in routes:
        score, solar, rain, solar_acc, rain_acc = score_route_with_forecast(route, collection_name)
        if score > best_score:
            best_score = score
            best_route = route
            best_solar = solar
            best_rain = rain
            best_solar_acc = solar_acc
            best_rain_acc = rain_acc

    if best_route:
         print_route_details(best_route, best_solar, best_rain, best_solar_acc, best_rain_acc)
    else:
        print("No route meets forecast accuracy threshold.")

    return best_route


# ---------------- LIVE MONITORING ----------------
def monitor_and_reroute(current_location, destination, collection_name, iterations=3):
    for _ in range(iterations): #Change this to while(True) When testing with censors
        solar, rain = fetch_live_weather(current_location['lat'], current_location['lon'])
        print(f"Live Solar: {solar:.1f}, Rain: {rain:.2f}")

        if solar < SOLAR_THRESHOLD or rain > RAIN_THRESHOLD:
            print("Conditions not optimal! Recalculating route based on forecast...")
            best_route = select_best_route(current_location, destination, collection_name)
            if best_route:
                print("New route selected!")
                for leg in best_route['legs']:
                    for step in leg['steps']:
                        print(step['html_instructions'] if isinstance(step, dict) else step)
            else:
                print("No alternative route available.")
        else:
            print("Current route is still optimal.")

        time.sleep(5)  # shorter sleep for testing

# ---------------- EXECUTE ----------------
if __name__ == "__main__":
    best_route = select_best_route(CURRENT_LOCATION, DESTINATION, "ESP32_data")
    if best_route:
        print("Initial Best Route:")
        for leg in best_route['legs']:
            for step in leg['steps']:
                print(step['html_instructions'] if isinstance(step, dict) else step)
        monitor_and_reroute(CURRENT_LOCATION, DESTINATION, "ESP32_data", iterations=3)
    else:
        print("No route available.")
