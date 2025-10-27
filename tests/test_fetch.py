# test_fetch.py
import sys
import os
sys.path.append(os.path.abspath(".."))

from backend_operations.Connections import list_collections, show_documents

# List all collections
list_collections()

# Show first 5 documents of a collection
show_documents("ESP32_data", limit=5)