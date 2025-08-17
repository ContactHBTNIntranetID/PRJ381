# main.py
import time
from backend_operations.Connections import client, DEFAULT_DB
from validator import Validator

# Function to fetch new documents from MongoDB
def fetch_documents(collection_name, last_id=None):
    """Fetch documents from MongoDB. Only new docs if last_id is given."""
    db = client[DEFAULT_DB]
    collection = db[collection_name]
    # If last_id is provided, fetch only newer documents
    cursor = collection.find({"_id": {"$gt": last_id}}) if last_id else collection.find()
    return list(cursor)

# Function to validate a single document's sensor data
def validate_document(doc, validator):
    """Validate a single document safely, handling missing fields."""
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

# Function to log invalid documents to a separate collection
def log_invalid_document(doc, validation_result):
    """Save invalid documents to a separate MongoDB collection."""
    db = client[DEFAULT_DB]
    invalid_collection = db["invalid_readings"]

    # Extract only invalid fields with reasons
    errors = {k: v["message"] for k, v in validation_result.items() if not v["valid"]}

    invalid_doc = {
        "original_document": doc,
        "errors": errors,
        "logged_at": time.strftime("%Y-%m-%d %H:%M:%S")
    }

    # Prevent duplicates
    if not invalid_collection.find_one({"original_document._id": doc["_id"]}):
        invalid_collection.insert_one(invalid_doc)
        print("⚠️ Logged invalid document to 'invalid_readings'.")

# Function to log valid documents to a separate collection
def log_valid_document(doc):
    """Save valid documents to a separate MongoDB collection."""
    db = client[DEFAULT_DB]
    valid_collection = db["valid_readings"]

    valid_doc = {
        "original_document": doc,
        "logged_at": time.strftime("%Y-%m-%d %H:%M:%S")
    }

    # Prevent duplicates
    if not valid_collection.find_one({"original_document._id": doc["_id"]}):
        valid_collection.insert_one(valid_doc)
        print("✅ Logged valid document to 'valid_readings'.")

# Print a summary of validation results to console
def print_summary(doc, result):
    """Print a concise summary of validation results for a document."""
    print(f"Document ID: {doc.get('_id')}")
    for key, val in result.items():
        status = "✅" if val["valid"] else "❌"
        print(f"{status} {key}: {val['message']}")
    print("-" * 50)

# Optional: print number of documents in each collection
def show_collection_counts():
    """Print number of documents in each collection."""
    db = client[DEFAULT_DB]
    print("\n📊 Collection counts:")
    for coll in db.list_collection_names():
        count = db[coll].count_documents({})
        print(f" - {coll}: {count} documents")

# Main loop: fetch, validate, log, and repeat
def main():
    validator = Validator()
    collection_name = "ESP32_data"
    last_id = None

    print("Starting continuous validation...\nPress Ctrl+C to stop.")
    try:
        while True:
            documents = fetch_documents(collection_name, last_id)
            if documents:
                for doc in documents:
                    # Validate the document
                    result = validate_document(doc, validator)
                    print_summary(doc, result)

                    # Log valid or invalid documents
                    if not all(v["valid"] for v in result.values()):
                        log_invalid_document(doc, result)
                    else:
                        log_valid_document(doc)

                # Update last processed ID
                last_id = documents[-1]["_id"]
                # Optional: see counts in each collection
                show_collection_counts()
            else:
                print("No new documents.")
            # Wait 5 seconds before next batch
            time.sleep(5)
    except KeyboardInterrupt:
        print("\nValidation stopped by user.")

if __name__ == "__main__":
     # main() # Commented out to prevent accidental DB writes
     pass

