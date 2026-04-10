import firebase_admin
from firebase_admin import credentials, firestore
from pymongo import MongoClient

# Initialize Firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
fs_db = firestore.client()

# Connect to MongoDB Atlas (replace <username>, <password>, and cluster info)
client = MongoClient("mongodb+srv://mihara:mihara1234@adb.jkbt625.mongodb.net/?appName=ADB")

# Create/use database and collection
mongo_db = client["tap_database"]       # new database inside ADB cluster
tap_logs_collection = mongo_db["tap_logs"]  # collection to hold tap logs
# Export Firestore -> MongoDB
docs = fs_db.collection("tap_logs").stream()
count = 0
for doc in docs:
    tap_logs_collection.insert_one(doc.to_dict())
    count += 1

print(f"Export complete. {count} documents copied to MongoDB Atlas.")
