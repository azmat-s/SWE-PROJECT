import os
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional
import logging
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

class Database:
    client: Optional[AsyncIOMotorClient] = None
    database = None

db = Database()

async def get_database():

    if db.database is None:
        await connect_to_database()
    return db.database

async def connect_to_database():

    try:
        # Get MongoDB connection string from environment
        mongodb_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
        database_name = os.getenv("DATABASE_NAME", "matchwise")
        
        logger.info(f"Connecting to MongoDB at {mongodb_url}")
        
        # Create motor client
        db.client = AsyncIOMotorClient(mongodb_url)
        
        # Get database
        db.database = db.client[database_name]
        
        # Test connection
        await db.database.command("ping")
        
        logger.info(f"Successfully connected to MongoDB database: {database_name}")
        
        # Create indexes
        await create_indexes()
        
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        raise

async def close_database_connection():

    try:
        if db.client:
            db.client.close()
            logger.info("MongoDB connection closed")
    except Exception as e:
        logger.error(f"Error closing MongoDB connection: {e}")

async def create_indexes():

    try:
        # Users collection indexes
        users_collection = db.database.users
        await users_collection.create_index("email", unique=True)
        await users_collection.create_index("role")
        await users_collection.create_index("is_active")
        
        # Compound index for recruiter searches
        await users_collection.create_index([("role", 1), ("company", 1)])
        
        # Compound index for job seeker searches
        await users_collection.create_index([("role", 1), ("skills", 1)])
        
        # Match results collection indexes
        match_results_collection = db.database.match_results
        await match_results_collection.create_index("application_id")
        await match_results_collection.create_index("job_id")
        await match_results_collection.create_index("user_id")
        await match_results_collection.create_index([("job_id", 1), ("overall_score", -1)])
        
        logger.info("Database indexes created successfully")
        
    except Exception as e:
        logger.error(f"Error creating indexes: {e}")