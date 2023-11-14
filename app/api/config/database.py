
from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

# Constants
DB_USERNAME = os.getenv('DB_USERNAME', '')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')
DB_URI = os.getenv('DB_URI', '')

client = MongoClient(f"mongodb+srv://{DB_USERNAME}:{DB_PASSWORD}@{DB_URI}/?retryWrites=true&w=majority")

db = client.nova_deriv_db

copier_collection = db["copier_collection"]
trader_collection = db["trader_collection"]
