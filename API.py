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

    # dumps converts MongoDB docs (with ObjectId, dates, etc.) into valid JSON
    return app.response_class(dumps(documents), mimetype="application/json")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)