import os
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv('REDIS_URL')
MONGO_URI = os.getenv('MONGO_URI')