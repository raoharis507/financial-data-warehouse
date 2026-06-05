from app.database.mongodb import MongoDB
from datetime import datetime
import uuid

# Connect to MongoDB
db = MongoDB.connect()

# Sample assets
sample_assets = [
    {
        "assetId": "AAPL",
        "symbol": "AAPL",
        "name": "Apple Inc.",
        "assetClass": "stock",
        "region": "US",
        "description": "Apple Inc. is an American multinational technology company",
        "provider": "Nasdaq",
        "validFrom": datetime.now(),
        "isDeleted": False,
        "metadata": {"sector": "Technology", "exchange": "NASDAQ"}
    },
    {
        "assetId": "MSFT",
        "symbol": "MSFT",
        "name": "Microsoft Corporation",
        "assetClass": "stock",
        "region": "US",
        "description": "Microsoft develops software, services, devices, and solutions",
        "provider": "Nasdaq",
        "validFrom": datetime.now(),
        "isDeleted": False,
        "metadata": {"sector": "Technology", "exchange": "NASDAQ"}
    },
    {
        "assetId": "BTC",
        "symbol": "BTC",
        "name": "Bitcoin",
        "assetClass": "crypto",
        "region": "Global",
        "description": "Decentralized digital currency",
        "provider": "Coinbase",
        "validFrom": datetime.now(),
        "isDeleted": False,
        "metadata": {"type": "Cryptocurrency", "market_cap": "Large"}
    }
]

# Sample data sources
sample_sources = [
    {
        "sourceId": "nasdaq_v1",
        "name": "Nasdaq Data Link",
        "baseUrl": "https://data.nasdaq.com/api/v3",
        "apiType": "REST",
        "authRequired": True,
        "supportedAssets": ["AAPL", "MSFT", "TSLA", "GOOGL"],
        "validFrom": datetime.now(),
        "isValid": True
    },
    {
        "sourceId": "bloomberg_v1",
        "name": "Bloomberg API",
        "baseUrl": "https://api.bloomberg.com",
        "apiType": "REST",
        "authRequired": True,
        "supportedAssets": ["AAPL", "MSFT", "BTC", "ETH"],
        "validFrom": datetime.now(),
        "isValid": True
    }
]

# Sample time series data (mock data for last 5 days)
sample_timeseries = []

for asset in ["AAPL", "MSFT"]:
    base_price = 150 if asset == "AAPL" else 280
    for i in range(5):
        date = datetime(2026, 5, 17 - i, 12, 0, 0)
        price = base_price + (i * 2)
        sample_timeseries.append({
            "dataPointId": str(uuid.uuid4()),
            "assetId": asset,
            "provider": "Nasdaq",
            "timestamp": date,
            "openPrice": price - 1,
            "highPrice": price + 2,
            "lowPrice": price - 2,
            "closePrice": price,
            "volume": 1000000 + (i * 100000),
            "adjustedClose": price,
            "source": "NASDAQ API",
            "ingestedAt": datetime.now(),
            "attributes": {"currency": "USD"}
        })

# Clear existing data (optional - be careful!)
db.assets.delete_many({})
db.datasources.delete_many({})
db.timeseries.delete_many({})

# Insert sample data
db.assets.insert_many(sample_assets)
db.datasources.insert_many(sample_sources)
db.timeseries.insert_many(sample_timeseries)

print(f"✓ Loaded {len(sample_assets)} assets")
print(f"✓ Loaded {len(sample_sources)} data sources")
print(f"✓ Loaded {len(sample_timeseries)} time series data points")
print("\nSample data loaded successfully!")
