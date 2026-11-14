import os
from dotenv import load_dotenv
from pymongo import AsyncMongoClient

load_dotenv()

client=AsyncMongoClient(os.getenv('MONGODB_URI'))
db=client[os.getenv('DATABASE_NAME')]
todo_collection=db['Todo-App']