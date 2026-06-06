from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from typing import List, Optional
from datetime import datetime
import uuid

from app.database.mongodb import MongoDB
from app.models.asset import Asset, AssetResponse, AssetDetailResponse
from app.models.timeseries import TimeSeriesPoint, TimeSeriesResponse
from app.models.datasource import DataSource, SourceResponse

app = FastAPI(title="Financial Data Warehouse API", version="1.0.0")

@app.on_event("startup")
async def startup_event():
    """Connect to MongoDB on startup"""
    MongoDB.connect()

@app.on_event("shutdown")
async def shutdown_event():
    """Close MongoDB connection on shutdown"""
    MongoDB.close()

@app.get("/")
async def root():
    return {"message": "Financial Data Warehouse API", "status": "running"}

# UC 2 - Q1: Return limited info about all financial assets
@app.get("/api/assets", response_model=List[AssetResponse])
async def get_all_assets(limit: int = Query(100, ge=1, le=1000)):
    """Return limited info about all financial assets"""
    db = MongoDB.get_db()
    assets = list(db.assets.find(
        {"isDeleted": False}, 
        {"assetId": 1, "symbol": 1, "name": 1, "assetClass": 1, "region": 1, "_id": 0}
    ).limit(limit))
    return assets

# UC 2 - Q2: Return all details of an asset by ID
@app.get("/api/assets/{asset_id}", response_model=AssetDetailResponse)
async def get_asset_details(asset_id: str):
    """Return all details of an asset"""
    db = MongoDB.get_db()
    asset = db.assets.find_one(
        {"assetId": asset_id, "isDeleted": False},
        {"_id": 0}
    )
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return asset

# UC 2 - Q3: Return limited info about all data sources
@app.get("/api/sources", response_model=List[SourceResponse])
async def get_all_sources():
    """Return limited info about all data sources"""
    db = MongoDB.get_db()
    sources = list(db.datasources.find(
        {"isValid": True},
        {"sourceId": 1, "name": 1, "apiType": 1, "_id": 0}
    ))
    return sources

# UC 2 - Q4: Return all details of a data source by ID
@app.get("/api/sources/{source_id}")
async def get_source_details(source_id: str):
    """Return all details of a data source"""
    db = MongoDB.get_db()
    source = db.datasources.find_one(
        {"sourceId": source_id, "isValid": True},
        {"_id": 0}
    )
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
    return source

# UC 2 - Q5: Return time-series data for specified asset and data source
@app.get("/api/timeseries/{asset_id}/{provider}", response_model=TimeSeriesResponse)
async def get_timeseries(
    asset_id: str, 
    provider: str,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    limit: int = Query(100, ge=1, le=10000)
):
    """Return time-series data for specified asset and data source"""
    db = MongoDB.get_db()
    
    query = {"assetId": asset_id, "provider": provider}
    if start_date or end_date:
        query["timestamp"] = {}
        if start_date:
            query["timestamp"]["$gte"] = start_date
        if end_date:
            query["timestamp"]["$lte"] = end_date
    
    data = list(db.timeseries.find(
        query,
        {"_id": 0, "dataPointId": 1, "timestamp": 1, "openPrice": 1, 
         "highPrice": 1, "lowPrice": 1, "closePrice": 1, "volume": 1, 
         "adjustedClose": 1, "attributes": 1}
    ).sort("timestamp", -1).limit(limit))
    
    return TimeSeriesResponse(assetId=asset_id, provider=provider, data=data)

# Health check endpoint
@app.get("/health")
async def health_check():
    db = MongoDB.get_db()
    try:
        db.command("ping")
        return {"status": "healthy", "database": "connected"}
    except:
        return {"status": "unhealthy", "database": "disconnected"}

# UC 1: Data Ingest from Financial Data Providers
async def ingest_data(asset_id: str, provider: str):
    """Ingest data from external provider for specified asset"""
    from app.services.ingestion import DataIngestionService
    result = await DataIngestionService.ingest_from_provider(asset_id, provider)
    return result

@app.get("/api/provenance/{asset_id}/{provider}")
async def get_provenance(asset_id: str, provider: str):
    """Get data provenance information"""
    from app.services.ingestion import DataIngestionService
    result = await DataIngestionService.get_provenance(asset_id, provider)
    return result

# UC 3: Analytics and Data Mining
@app.get("/api/analytics/ma/{asset_id}/{provider}")
async def moving_average(asset_id: str, provider: str, days: int = 5):
    """Calculate moving average for asset"""
    from app.services.analytics import AnalyticsService
    return await AnalyticsService.calculate_moving_average(asset_id, provider, days)

@app.get("/api/analytics/forecast/{asset_id}/{provider}")
async def forecast(asset_id: str, provider: str, days_ahead: int = 1):
    """Forecast future prices using linear regression"""
    from app.services.analytics import AnalyticsService
    return await AnalyticsService.forecast_price(asset_id, provider, days_ahead)

@app.get("/api/analytics/volatility/{asset_id}/{provider}")
async def volatility(asset_id: str, provider: str):
    """Calculate price volatility and risk assessment"""
    from app.services.analytics import AnalyticsService
    return await AnalyticsService.price_volatility(asset_id, provider)

# UC 4: LLM-powered Assistant

# UC 4: LLM-powered Assistant

# UC 4: LLM-powered Assistant (using GET for easy testing)
@app.get("/api/assistant/ask")

# UC 4: LLM-powered Assistant
@app.get("/api/assistant/ask")
async def ask_assistant(query: str):
    """Ask the LLM assistant a natural language question"""
    from app.services.llm_assistant import LLMAssistant
    result = await LLMAssistant.process_query(query)
    return result

# Spark Analytics Endpoints (M6 & M7)
@app.get("/api/spark/ma/{asset_id}/{provider}")
async def spark_moving_average(asset_id: str, provider: str, days: int = 5):
    """Moving average using Apache Spark"""
    from app.services.spark_analytics import SparkAnalyticsService
    return await SparkAnalyticsService.calculate_moving_average_spark(asset_id, provider, days)

@app.get("/api/spark/forecast/{asset_id}/{provider}")
async def spark_forecast(asset_id: str, provider: str, days_ahead: int = 3):
    """Price forecast using Apache Spark MLlib"""
    from app.services.spark_analytics import SparkAnalyticsService
    return await SparkAnalyticsService.forecast_price_spark(asset_id, provider, days_ahead)

# Real Data Ingestion with Yahoo Finance (Idempotent)
@app.post("/api/ingest/real/{asset_symbol}")
async def ingest_real_data(asset_symbol: str):
    """Ingest real data from Yahoo Finance API (idempotent - no duplicates)"""
    from app.services.real_ingestion import RealIngestionService
    result = await RealIngestionService.ingest_from_yahoo(asset_symbol)
    return result

@app.get("/api/ingest/check/{asset_symbol}/{date}")
async def check_idempotent(asset_symbol: str, date: str):
    """Check if data already exists for a specific date"""
    from app.services.real_ingestion import RealIngestionService
    result = await RealIngestionService.get_idempotent_ingest(asset_symbol, date)
    return result

# Provider-Agnostic Ingestion (Easy to add new providers)
@app.post("/api/ingest/provider/{asset_symbol}/{provider_name}")
async def ingest_from_provider(asset_symbol: str, provider_name: str):
    """Ingest data from any registered provider (yahoo, mock)"""
    from app.services.provider_interface import ProviderIngestionService
    result = await ProviderIngestionService.ingest_from_provider(asset_symbol, provider_name)
    return result

@app.get("/api/providers")
async def list_providers():
    """List all registered providers"""
    from app.services.provider_interface import ProviderIngestionService
    return {"providers": list(ProviderIngestionService._providers.keys())}
