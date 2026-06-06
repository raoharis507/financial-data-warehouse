import yfinance as yf
from datetime import datetime, timedelta
import uuid
from app.database.mongodb import MongoDB

class RealIngestionService:
    
    @staticmethod
    async def ingest_from_yahoo(asset_symbol: str):
        """Ingest real data from Yahoo Finance API"""
        db = MongoDB.get_db()
        
        try:
            # Download real data from Yahoo Finance
            ticker = yf.Ticker(asset_symbol)
            
            # Get historical data for last 7 days
            end_date = datetime.now()
            start_date = end_date - timedelta(days=7)
            
            hist = ticker.history(start=start_date, end=end_date)
            
            if hist.empty:
                return {"status": "error", "message": f"No data found for {asset_symbol}"}
            
            # Check for duplicates before inserting
            existing_dates = set()
            existing_records = db.timeseries.find(
                {"assetId": asset_symbol, "provider": "YahooFinance"},
                {"timestamp": 1}
            )
            for record in existing_records:
                if record.get("timestamp"):
                    existing_dates.add(record["timestamp"].strftime("%Y-%m-%d"))
            
            # Insert only new data points (idempotent)
            ingested_count = 0
            for index, row in hist.iterrows():
                date_str = index.strftime("%Y-%m-%d")
                
                # Skip if already exists (idempotent)
                if date_str in existing_dates:
                    continue
                
                point = {
                    "dataPointId": str(uuid.uuid4()),
                    "assetId": asset_symbol,
                    "provider": "YahooFinance",
                    "timestamp": index,
                    "openPrice": float(row['Open']),
                    "highPrice": float(row['High']),
                    "lowPrice": float(row['Low']),
                    "closePrice": float(row['Close']),
                    "volume": float(row['Volume']),
                    "source": "Yahoo Finance API",
                    "ingestedAt": datetime.now(),
                    "attributes": {
                        "currency": "USD",
                        "data_quality": "real",
                        "dividends": float(row.get('Dividends', 0)),
                        "stock_splits": float(row.get('Stock Splits', 0))
                    }
                }
                db.timeseries.insert_one(point)
                ingested_count += 1
            
            return {
                "status": "success",
                "ingested": ingested_count,
                "asset": asset_symbol,
                "provider": "YahooFinance",
                "message": f"Real data from Yahoo Finance. New records: {ingested_count}"
            }
            
        except Exception as e:
            return {"status": "error", "message": str(e), "asset": asset_symbol}
    
    @staticmethod
    async def get_idempotent_ingest(asset_symbol: str, date: str):
        """Check if data already exists for a specific date (idempotency check)"""
        db = MongoDB.get_db()
        
        # Parse date
        target_date = datetime.strptime(date, "%Y-%m-%d")
        
        # Check if record exists
        existing = db.timeseries.find_one({
            "assetId": asset_symbol,
            "provider": "YahooFinance",
            "timestamp": {
                "$gte": target_date,
                "$lt": target_date + timedelta(days=1)
            }
        })
        
        return {
            "asset": asset_symbol,
            "date": date,
            "exists": existing is not None,
            "record_id": existing.get("dataPointId") if existing else None
        }
