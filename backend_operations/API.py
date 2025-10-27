from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson.json_util import dumps

app = Flask(__name__)

MONGO_URI = "mongodb+srv://oarabilembewe:VKTI012h0T3BGZ9J@ecommerce-cluster.4nb3ndy.mongodb.net/"
DEFAULT_DB = "PRJ382_DB"
client = MongoClient(MONGO_URI)
db = client[DEFAULT_DB]


@app.route("/collections", methods=["GET"])
def list_collections():
    collections = db.list_collection_names()
    return jsonify({"collections": collections})


@app.route("/documents/<collection_name>", methods=["GET"])
def show_documents(collection_name):
    limit = request.args.get("limit", default=0, type=int)
    collection = db[collection_name]
    cursor = collection.find()
    if limit > 0:
        cursor = cursor.limit(limit)

    documents = list(cursor)
    if not documents:
        return jsonify({"message": f"No documents found in '{collection_name}'"})

    return app.response_class(dumps(documents), mimetype="application/json")


# Import your predictive analysis function
from PredictiveAnalysis import run_predictive_analysis, API_AVG_SOLAR, API_AVG_RAIN, API_Instructions, API_RAIN_ACC, API_SCORE_ACC, API_SOLAR_ACC, API_TOTAL_DISTANCE, API_TOTAL_DURATION

@app.route("/analysis", methods=["GET"])
def get_analysis():
    # Run the predictive analysis
    run_predictive_analysis()

    # Return JSON-safe dictionary
    return jsonify({
        "average_solar": float(API_AVG_SOLAR),
        "average_rain": float(API_AVG_RAIN),
        "instructions": [str(i) for i in API_Instructions],  # convert instructions to strings
        "rain_accuracy": float(API_RAIN_ACC),
        "score_accuracy": float(API_SCORE_ACC),
        "solar_accuracy": float(API_SOLAR_ACC),
        "total_distance": str(API_TOTAL_DISTANCE),
        "total_duration": str(API_TOTAL_DURATION)
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
