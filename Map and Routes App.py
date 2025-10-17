from flask import Flask, jsonify, request, current_app
from pymongo import MongoClient
from bson.json_util import dumps
import os
import requests
import logging

app = Flask(__name__)

# Configuration from environment
MONGO_URI = os.getenv("MONGO_URI")
DEFAULT_DB = os.getenv("DEFAULT_DB", "PRJ382_DB")
MAPBOX_ACCESS_TOKEN = os.getenv("MAPBOX_ACCESS_TOKEN")

# Logging
logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger("flask-map-api")

if not MONGO_URI:
    logger.warning("MONGO_URI not set. Defaulting to localhost (development only).")
    MONGO_URI = "mongodb://localhost:27017"

# Create Mongo client with sensible timeouts
try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000, connectTimeoutMS=5000)
    # Optional: ping to fail fast
    client.admin.command("ping")
    db = client[DEFAULT_DB]
    logger.info("Connected to MongoDB")
except Exception as e:
    logger.exception("Could not connect to MongoDB on startup: %s", e)
    client = None
    db = None

def is_valid_coord(lat, lng):
    try:
        lat = float(lat)
        lng = float(lng)
        return -90 <= lat <= 90 and -180 <= lng <= 180
    except (TypeError, ValueError):
        return False

@app.route("/collections", methods=["GET"])
def list_collections():
    if db is None:
        return jsonify({"error": "Database not configured"}), 500
    try:
        collections = db.list_collection_names()
        return jsonify({"collections": collections})
    except Exception as e:
        logger.exception("Error listing collections")
        return jsonify({"error": str(e)}), 500

@app.route("/documents/<collection_name>", methods=["GET"])
def show_documents(collection_name):
    if db is None:
        return jsonify({"error": "Database not configured"}), 500
    try:
        limit = request.args.get("limit", default=100, type=int)
        skip = request.args.get("skip", default=0, type=int)
        max_limit = 1000
        if limit < 0:
            limit = 0
        if limit > max_limit:
            limit = max_limit

        collection = db[collection_name]
        cursor = collection.find().skip(skip)
        if limit > 0:
            cursor = cursor.limit(limit)

        documents = list(cursor)
        if not documents:
            return jsonify({"message": f"No documents found in '{collection_name}'"}), 404

        return current_app.response_class(dumps(documents), mimetype="application/json")
    except Exception as e:
        logger.exception("Error fetching documents from collection %s", collection_name)
        return jsonify({"error": str(e)}), 500

@app.route("/api/directions", methods=["POST"])
def get_directions():
    if not MAPBOX_ACCESS_TOKEN:
        logger.error("Mapbox token not configured")
        return jsonify({"error": "Mapbox token not configured on server"}), 500

    if not request.is_json:
        return jsonify({"error": "Request body must be JSON"}), 400

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid JSON body"}), 400

    start = data.get("start")
    end = data.get("end")
    if not start or not end:
        return jsonify({"error": "Missing 'start' or 'end' in request body"}), 400

    try:
        s_lat = float(start.get("lat"))
        s_lng = float(start.get("lng"))
        e_lat = float(end.get("lat"))
        e_lng = float(end.get("lng"))
    except Exception:
        return jsonify({"error": "start/end must include numeric lat and lng"}), 400

    if not is_valid_coord(s_lat, s_lng) or not is_valid_coord(e_lat, e_lng):
        return jsonify({"error": "Invalid coordinates"}), 400

    coords = f"{s_lng},{s_lat};{e_lng},{e_lat}"
    url = f"https://api.mapbox.com/directions/v5/mapbox/driving/{coords}"
    params = {"alternatives": "true", "geometries": "geojson", "access_token": MAPBOX_ACCESS_TOKEN}

    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        if data.get("code") != "Ok":
            return jsonify({"error": "No routes found", "mapbox_code": data.get("code")}), 400

        routes = []
        for i, route in enumerate(data.get("routes", [])):
            routes.append({
                "id": i,
                "geometry": route.get("geometry"),
                "distance_m": route.get("distance"),
                "duration_s": route.get("duration"),
                "summary": route.get("summary")
            })
        return jsonify({"routes": routes})
    except requests.exceptions.Timeout:
        logger.exception("Mapbox request timed out")
        return jsonify({"error": "Mapbox request timed out"}), 504
    except requests.exceptions.RequestException as e:
        logger.exception("Mapbox request failed: %s", e)
        return jsonify({"error": "Mapbox request failed"}), 502
    except ValueError:
        logger.exception("Mapbox returned non-JSON response")
        return jsonify({"error": "Mapbox returned an unexpected response"}), 502
    except Exception as e:
        logger.exception("Unhandled error in /api/directions: %s", e)
        return jsonify({"error": "Internal server error"}), 500

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "OK", "service": "Flask Map API", "db_connected": db is not None})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=os.getenv("FLASK_DEBUG", "false").lower() in ("1","true"))
