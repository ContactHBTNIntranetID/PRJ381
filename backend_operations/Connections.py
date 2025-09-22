from pymongo import MongoClient
from tabulate import tabulate

MONGO_URI = "mongodb+srv://oarabilembewe:VKTI012h0T3BGZ9J@ecommerce-cluster.4nb3ndy.mongodb.net/"
DEFAULT_DB = "PRJ382_DB"
client = MongoClient(MONGO_URI)

#lists all my collections in the database
def list_collections():
    """Print collections in the default database."""
    collections = client[DEFAULT_DB].list_collection_names()
    print(f"Collections in '{DEFAULT_DB}':")
    for coll in collections:
        print(f"- {coll}")

#This will have all the data within the collection that you chose
def show_documents(collection_name, limit=None):
    """Print documents from a collection in tabular form."""
    db = client[DEFAULT_DB]
    collection = db[collection_name]
    cursor = collection.find()
    if limit:
        cursor = cursor.limit(limit)
    documents = list(cursor)
    if not documents:
        print(f"No documents found in collection '{collection_name}'.")
        return
    # Convert ObjectId to string for display
    for doc in documents:
        if '_id' in doc:
            doc['_id'] = str(doc['_id'])
    # Prepare table
    headers = documents[0].keys()
    rows = [doc.values() for doc in documents]
    print(f"Documents in collection '{collection_name}':")
    print(tabulate(rows, headers=headers, tablefmt="grid"))


#same function just that this one has a return type per line
def return_documents(collection_name, limit=None):
    """Return documents from a collection in tabular form."""
    db = client[DEFAULT_DB]
    collection = db[collection_name]
    cursor = collection.find()
    if limit:
        cursor = cursor.limit(limit)
    documents = list(cursor)
    if not documents:
        print(f"No documents found in collection '{collection_name}'.")
        return []
    # Convert ObjectId to string for display
    for doc in documents:
        if '_id' in doc:
            doc['_id'] = str(doc['_id'])
    return documents








