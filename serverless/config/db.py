import os
import urllib.parse
import certifi

from pymongo import MongoClient
from dotenv import load_dotenv

import logging

load_dotenv()

DB_NAME = os.getenv("DB_NAME", "tasks_manager")
DB_USERNAME = os.getenv("DB_USERNAME", "")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")

MONGO_URI = f"mongodb+srv://{DB_USERNAME}:{DB_PASSWORD}@cluster0.bgi9bsb.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
ca = certifi.where()


def connect_db():
    try:
        client = MongoClient(MONGO_URI, tlsCAFile=ca)
        db = client[DB_NAME]
    except ConnectionError:
        logging.error("Failed to connect to the database")
    return db
