
import os
import ssl
import certifi
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv(".env")

uri = os.getenv("MONGO_URI")

print("Mongo URI found:", bool(uri))
print("OpenSSL:", ssl.OPENSSL_VERSION)

try:
    client = MongoClient(
        uri,
        tls=True,
        tlsCAFile=certifi.where(),
        serverSelectionTimeoutMS=15000
    )

    print("Testing MongoDB connection...")
    print(client.admin.command("ping"))
    print("MongoDB Atlas connected successfully!")

except Exception as e:
    print("Connection failed:")
    print(type(e).__name__)
    print(str(e))

finally:
    if "client" in locals():
        client.close()
