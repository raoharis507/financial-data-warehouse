import httpx
from datetime import datetime
import uuid
from app.database.mongodb import MongoDB

class DataIngestionService:
    @staticmethod
    async def ingest_from_provider(asset_symbol: str, provider: str):
        """Simulate ingesting data from external provider"""
        db = MongoDB.get_db()
        
        # Simulate API call to external provider
        # In production, this would call real APIs like:
        # - https://data.nasdaq.com/api/v3/datasets/...
        # - https://api.coingecko.com/api/v3/...
        
        # Mock data for demonstration
        mock_data = []
        base_price = 150 if asset_symbol == "AAPL" else (280 if asset_symbol == "MSFT" else 50000)
        
        for i in range(7):  # Last 7 days
            date = datetime.now()
            price = base_price + (i * 1.5)
            mock_data.append({
                "dataPointId": str(uuid.uuid4()),
                "assetId": asset_symbol,
                "provider": provider,
                "timestamp": date,
                "openPrice": price - 0.5,
                "highPrice": price + 1,
                "lowPrice": price - 1,
                "closePrice": price,
                "volume": 1000000 + (i * 50000),
                "source": f"{provider} API",
                "ingestedAt": datetime.now(),
                "attributes": {"currency": "USD", "data_quality": "high"}
            })
        
        # Insert into database (temporal: never overwrite, always add new)
        if mock_data:
            db.timeseries.insert_many(mock_data)
            return {"status": "success", "ingested": len(mock_data), "asset": asset_symbol}
        return {"status": "error", "message": "No data ingested"}
    
    @staticmethod
    async def get_provenance(asset_id: str, provider: str):
        """Get data provenance information"""
        db = MongoDB.get_db()
        provenance = list(db.timeseries.find(
            {"assetId": asset_id, "provider": provider},
            {"source": 1, "ingestedAt": 1, "provider": 1, "_id": 0}
        ).distinct("source"))
        
        return {
            "assetId": asset_id,
            "provider": provider,
            "sources": provenance,
            "temporal_records": db.timeseries.count_documents({"assetId": asset_id, "provider": provider})
        }
