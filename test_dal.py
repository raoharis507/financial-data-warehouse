import unittest
from app.database.mongodb import MongoDB
from app.models.asset import Asset
from app.models.timeseries import TimeSeriesPoint
from datetime import datetime
import uuid

class TestDataAccessLayer(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.db = MongoDB.connect()
        cls.test_asset_id = "TEST_" + str(uuid.uuid4())[:8]
    
    def test_1_insert_asset(self):
        """Test inserting an asset"""
        asset = {
            "assetId": self.test_asset_id,
            "symbol": "TEST",
            "name": "Test Asset",
            "assetClass": "stock",
            "region": "US",
            "provider": "TestProvider",
            "validFrom": datetime.now(),
            "isDeleted": False
        }
        result = self.db.assets.insert_one(asset)
        self.assertIsNotNone(result.inserted_id)
    
    def test_2_find_asset(self):
        """Test finding an asset"""
        asset = self.db.assets.find_one({"assetId": self.test_asset_id})
        self.assertIsNotNone(asset)
        self.assertEqual(asset["symbol"], "TEST")
    
    def test_3_insert_timeseries(self):
        """Test inserting time series data (temporal pattern)"""
        point = {
            "dataPointId": str(uuid.uuid4()),
            "assetId": self.test_asset_id,
            "provider": "TestProvider",
            "timestamp": datetime.now(),
            "closePrice": 100.00,
            "source": "UnitTest",
            "ingestedAt": datetime.now()
        }
        result = self.db.timeseries.insert_one(point)
        self.assertIsNotNone(result.inserted_id)
    
    def test_4_find_latest_timeseries(self):
        """Test findLatest pattern - should return most recent records"""
        # Insert multiple records
        for i in range(3):
            point = {
                "dataPointId": str(uuid.uuid4()),
                "assetId": self.test_asset_id,
                "provider": "TestProvider",
                "timestamp": datetime.now(),
                "closePrice": 100.00 + i,
                "source": "UnitTest",
                "ingestedAt": datetime.now()
            }
            self.db.timeseries.insert_one(point)
        
        # Query sorted by timestamp descending (latest first)
        results = list(self.db.timeseries.find(
            {"assetId": self.test_asset_id}
        ).sort("timestamp", -1).limit(1))
        
        self.assertGreater(len(results), 0)
    
    def test_5_soft_delete(self):
        """Test soft delete pattern"""
        self.db.assets.update_one(
            {"assetId": self.test_asset_id},
            {"$set": {"isDeleted": True, "validTo": datetime.now()}}
        )
        
        # Query should not return deleted assets
        active = self.db.assets.find_one({"assetId": self.test_asset_id, "isDeleted": False})
        self.assertIsNone(active)
    
    @classmethod
    def tearDownClass(cls):
        """Clean up test data"""
        cls.db.assets.delete_many({"assetId": cls.test_asset_id})
        cls.db.timeseries.delete_many({"assetId": cls.test_asset_id})

if __name__ == "__main__":
    unittest.main()
