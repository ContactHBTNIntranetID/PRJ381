#This should be something that ensures that given specific parameters of weather then we are able to tell if this the route that is being taken is appropriate or not
from pymongo import MongoClient
from tabulate import tabulate
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from Connections import return_documents



# Predictive analysis for solar vehicle route optimality
# minutes ahead specifies how many minutes ahead of time you would like to calculate for

def predict_route_optimality(collection_name, minutes_ahead=10):
    # Retrieve data
    documents = return_documents(collection_name) 
    if not documents:
        return

    # Extract time, solar irradiance, and rainfall
    times = []
    solar_irradiance = []
    rainfall = []
    for doc in documents:
        times.append(datetime.fromisoformat(doc['timestamp'].replace('Z', '+00:00')))
        solar_irradiance.append(doc['solar_irradiance_wm2'])
        rainfall.append(doc['rainfall_mm'])

    # Convert to numpy arrays
    solar_irradiance = np.array(solar_irradiance)
    rainfall = np.array(rainfall)
    times = np.array(times)

    # Fit ARIMA models
    model_solar = ARIMA(solar_irradiance, order=(1, 1, 1))  # (p,d,q) parameters, adjust as needed
    model_rain = ARIMA(rainfall, order=(1, 1, 1))
    fit_solar = model_solar.fit()
    fit_rain = model_rain.fit()

    # Forecast next 'minutes_ahead' minutes
    forecast_solar = fit_solar.forecast(steps=minutes_ahead)
    forecast_rain = fit_rain.forecast(steps=minutes_ahead)
    forecast_times = [times[-1] + timedelta(minutes=i+1) for i in range(minutes_ahead)]

    # Calculate averages
    avg_forecast_solar = np.mean(forecast_solar)
    avg_forecast_rain = np.mean(forecast_rain)

    # Optimality thresholds
    solar_threshold = 800  # W/m²
    rain_threshold = 1    # mm

    # Check optimality
    is_optimal_solar = avg_forecast_solar > solar_threshold
    is_optimal_rain = avg_forecast_rain < rain_threshold
    is_optimal = is_optimal_solar and is_optimal_rain

    # Output results
    print(f"Route Optimality Analysis (Next {minutes_ahead} Minutes):")
    print(tabulate([
        ["Solar Irradiance (W/m²)", f"{avg_forecast_solar:.1f}", f">{solar_threshold}", is_optimal_solar],
        ["Rainfall (mm)", f"{avg_forecast_rain:.2f}", f"<{rain_threshold}", is_optimal_rain]
    ], headers=["Metric", "Forecasted Average", "Threshold", "Meets Threshold"], tablefmt="grid"))
    print(f"Overall Route Optimality: {'Optimal' if is_optimal else 'Not Optimal'}")

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(times, solar_irradiance, label="Historical Solar Irradiance")
    plt.plot(forecast_times, forecast_solar, label="Forecasted Solar Irradiance", linestyle="--")
    plt.plot(times, rainfall, label="Historical Rainfall", color="orange")
    plt.plot(forecast_times, forecast_rain, label="Forecasted Rainfall", linestyle="--", color="orange")
    plt.xlabel("Time")
    plt.ylabel("Value")
    plt.title("Solar Irradiance and Rainfall Forecast")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Execute analysis
if __name__ == "__main__":
    collection_name = "ESP32_data"  
    predict_route_optimality(collection_name)