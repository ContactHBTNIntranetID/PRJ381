# test_invalid_log.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend_operations.Connections import client, DEFAULT_DB
from validator import Validator
import time

validator = Validator()
db = client[DEFAULT_DB]
invalid_collection = db["invalid_readings"]

# Fake invalid document
doc = {
    "temperature_c": "hot",
    "humidity_percent": -10,
    "pressure_hpa": 2000,
    "rainfall_mm": -5,
    "gps": {"lat": 100, "lon": 200}
}

# Validate
gps = doc.get("gps", {})
result = {
    "temperature": validator.validate_temperature(doc.get("temperature_c")),
    "humidity": validator.validate_humidity(doc.get("humidity_percent")),
    "pressure": validator.validate_pressure(doc.get("pressure_hpa")),
    "rainfall": validator.validate_rainfall(doc.get("rainfall_mm")),
    "gps": validator.validate_gps_coordinates(gps.get("lat"), gps.get("lon"))
}

# Log invalid
errors = {k: v["message"] for k, v in result.items() if not v["valid"]}
invalid_doc = {
    "original_document": doc,
    "errors": errors,
    "logged_at": time.strftime("%Y-%m-%d %H:%M:%S")
}
invalid_collection.insert_one(invalid_doc)
print("Invalid document logged:", invalid_doc)
