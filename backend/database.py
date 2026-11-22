
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME", "event_planner")

if not MONGO_URI:
    raise ValueError("MONGO_URI is missing. Check your .env file.")

client = MongoClient(
    MONGO_URI,
    serverSelectionTimeoutMS=10000
)

db = client[DATABASE_NAME]

# Collections
events_collection = db["events"]
venues_collection = db["venues"]
vendors_collection = db["vendors"]
guests_collection = db["guests"]
budgets_collection = db["budgets"]


# Check MongoDB connection
def check_database_connection():
    try:
        client.admin.command("ping")
        return True
    except Exception as e:
        print("Database connection error:", e)
        return False
