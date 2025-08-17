# main_safe_test.py
import time
from backend_operations.Connections import client, DEFAULT_DB
from validator import Validator

# Fetch documents like before
def fetch_documents(collection_name, last_id=None):
    db = client[DEFAULT_DB]
    collection = db[collection_name]
    cursor = collection.find({"_id": {"$gt": last_id}}) if last_id else collection.find()
    return list(cursor)

# Validate a document
def validate_document(doc, validator):
    gps = doc.get("gps", {})
    return {
        "temperature": validator.validate_temperature(doc.get("temperature_c")) 
                       if "temperature_c" in doc else {"valid": False, "message": "Temperature missing."},
        "humidity": validator.validate_humidity(doc.get("humidity_percent")) 
                    if "humidity_percent" in doc else {"valid": False, "message": "Humidity missing."},
        "pressure": validator.validate_pressure(doc.get("pressure_hpa")) 
                    if "pressure_hpa" in doc else {"valid": False, "message": "Pressure missing."},
        "rainfall": validator.validate_rainfall(doc.get("rainfall_mm")) 
                    if "rainfall_mm" in doc else {"valid": False, "message": "Rainfall missing."},
        "gps": validator.validate_gps_coordinates(gps.get("lat"), gps.get("lon")) 
               if "lat" in gps and "lon" in gps else {"valid": False, "message": "GPS coordinates missing."}
    }

# Print validation summary
def print_summary(doc, result):
    print(f"Document ID: {doc.get('_id')}")
    for key, val in result.items():
        status = "✅" if val["valid"] else "❌"
        print(f"{status} {key}: {val['message']}")
    print("-" * 50)

# Show counts of documents in each collection (optional)
def show_collection_counts():
    db = client[DEFAULT_DB]
    print("\n📊 Collection counts:")
    for coll in db.list_collection_names():
        count = db[coll].count_documents({})
        print(f" - {coll}: {count} documents")

def main():
    validator = Validator()
    collection_name = "ESP32_data"
    last_id = None

    print("Starting SAFE TEST validation (no data will be written)...\nPress Ctrl+C to stop.")
    try:
        while True:
            documents = fetch_documents(collection_name, last_id)
            if documents:
                for doc in documents:
                    result = validate_document(doc, validator)
                    print_summary(doc, result)

                last_id = documents[-1]["_id"]
                show_collection_counts()
            else:
                print("No new documents.")
            time.sleep(5)
    except KeyboardInterrupt:
        print("\nSAFE TEST validation stopped by user.")

if __name__ == "__main__":
    main()
