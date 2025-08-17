# test_validate_flow.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend_operations.Connections import client, DEFAULT_DB
from validator import Validator

validator = Validator()
db = client[DEFAULT_DB]
collection = db["ESP32_data"]

# Fetch one document
doc = collection.find_one()
print("Document:", doc)

# Validate
gps = doc.get("gps", {})
result = {
    "temperature": validator.validate_temperature(doc.get("temperature_c")),
    "humidity": validator.validate_humidity(doc.get("humidity_percent")),
    "pressure": validator.validate_pressure(doc.get("pressure_hpa")),
    "rainfall": validator.validate_rainfall(doc.get("rainfall_mm")),
    "gps": validator.validate_gps_coordinates(gps.get("lat"), gps.get("lon"))
}

print("Validation result:", result)
