from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import os
from dotenv import load_dotenv

load_dotenv()

class MongoDB:
    client = None
    db = None
    
    @classmethod
    def connect(cls):
        """Connect to MongoDB"""
        try:
            mongodb_uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017')
            database_name = os.getenv('DATABASE_NAME', 'financial_dwh')
            
            cls.client = MongoClient(mongodb_uri)
            cls.db = cls.client[database_name]
            
            # Test connection
            cls.client.admin.command('ping')
            print(f"✓ Connected to MongoDB database: {database_name}")
            return cls.db
        except ConnectionFailure as e:
            print(f"✗ Failed to connect to MongoDB: {e}")
            return None
    
    @classmethod
    def get_db(cls):
        """Get database instance"""
        if cls.db is None:
            cls.connect()
        return cls.db
    
    @classmethod
    def close(cls):
        """Close MongoDB connection"""
        if cls.client:
            cls.client.close()
            print("✓ MongoDB connection closed")
