# app/database.py
import os
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "matchwise")

# Async client for Motor (async operations)
async_client = None
database = None

async def get_database():
    global async_client, database
    if async_client is None:
        async_client = AsyncIOMotorClient(MONGODB_URL)
        database = async_client[DATABASE_NAME]
    return database

# Sync client for regular operations (if needed)
sync_client = None
sync_database = None

def get_sync_database():
    global sync_client, sync_database
    if sync_client is None:
        sync_client = MongoClient(MONGODB_URL)
        sync_database = sync_client[DATABASE_NAME]
    return sync_database

async def close_database():
    global async_client
    if async_client:
        async_client.close()
        async_client = None