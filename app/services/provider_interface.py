from abc import ABC, abstractmethod
import yfinance as yf
from datetime import datetime, timedelta
import uuid
from app.database.mongodb import MongoDB

class DataProvider(ABC):
    """Abstract base class for all data providers"""
    
    @abstractmethod
    async def fetch_data(self, asset_symbol: str, start_date: datetime, end_date: datetime):
        pass
    
    @abstractmethod
    def get_provider_name(self) -> str:
        pass

class YahooFinanceProvider(DataProvider):
    """Yahoo Finance implementation"""
    
    async def fetch_data(self, asset_symbol: str, start_date: datetime, end_date: datetime):
        ticker = yf.Ticker(asset_symbol)
        hist = ticker.history(start=start_date, end=end_date)
        return hist
    
    def get_provider_name(self) -> str:
        return "YahooFinance"

class MockProvider(DataProvider):
    """Mock provider for testing"""
    
    async def fetch_data(self, asset_symbol: str, start_date: datetime, end_date: datetime):
        # Generate mock data
        import pandas as pd
        dates = pd.date_range(start=start_date, end=end_date, freq='D')
        data = []
        for i, date in enumerate(dates):
            data.append({
                'Open': 100 + i,
                'High': 105 + i,
                'Low': 95 + i,
                'Close': 102 + i,
                'Volume': 1000000
            })
        return data
    
    def get_provider_name(self) -> str:
        return "MockProvider"

class ProviderIngestionService:
    """Provider-agnostic ingestion service - easily add new providers"""
    
    _providers = {}
    
    @classmethod
    def register_provider(cls, name: str, provider: DataProvider):
        """Register a new provider dynamically"""
        cls._providers[name] = provider
    
    @classmethod
    async def ingest_from_provider(cls, asset_symbol: str, provider_name: str):
        """Ingest data from any registered provider"""
        db = MongoDB.get_db()
        
        if provider_name not in cls._providers:
            return {"status": "error", "message": f"Provider {provider_name} not registered"}
        
        provider = cls._providers[provider_name]
        
        # Check for existing data (idempotent)
        existing_dates = set()
        existing_records = db.timeseries.find(
            {"assetId": asset_symbol, "provider": provider.get_provider_name()},
            {"timestamp": 1}
        )
        for record in existing_records:
            if record.get("timestamp"):
                existing_dates.add(record["timestamp"].strftime("%Y-%m-%d"))
        
        # Fetch data
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        data = await provider.fetch_data(asset_symbol, start_date, end_date)
        
        ingested_count = 0
        for item in data:
            if hasattr(item, 'name'):  # Pandas Series
                date_str = item.name.strftime("%Y-%m-%d")
                if date_str in existing_dates:
                    continue
                    
                point = {
                    "dataPointId": str(uuid.uuid4()),
                    "assetId": asset_symbol,
                    "provider": provider.get_provider_name(),
                    "timestamp": item.name,
                    "openPrice": float(item['Open']),
                    "highPrice": float(item['High']),
                    "lowPrice": float(item['Low']),
                    "closePrice": float(item['Close']),
                    "volume": float(item['Volume']),
                    "source": f"{provider.get_provider_name()} API",
                    "ingestedAt": datetime.now(),
                    "attributes": {"currency": "USD"}
                }
                db.timeseries.insert_one(point)
                ingested_count += 1
        
        return {
            "status": "success",
            "ingested": ingested_count,
            "asset": asset_symbol,
            "provider": provider.get_provider_name()
        }

# Register providers
ProviderIngestionService.register_provider("yahoo", YahooFinanceProvider())
ProviderIngestionService.register_provider("mock", MockProvider())
