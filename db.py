from pymongo import MongoClient
from utils.config import MONGO_URI

conn = MongoClient(str(MONGO_URI))

db = conn.tika
