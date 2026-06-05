import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta
from app.database.mongodb import MongoDB

class AnalyticsService:
    @staticmethod
    async def calculate_moving_average(asset_id: str, provider: str, days: int = 5):
        """Calculate moving average of closing prices"""
        db = MongoDB.get_db()
        data = list(db.timeseries.find(
            {"assetId": asset_id, "provider": provider},
            {"closePrice": 1, "timestamp": 1, "_id": 0}
        ).sort("timestamp", -1).limit(days))
        
        if len(data) < 2:
            return {"error": "Insufficient data"}
        
        prices = [d['closePrice'] for d in data]
        avg_price = np.mean(prices)
        
        return {
            "assetId": asset_id,
            "period_days": days,
            "moving_average": round(avg_price, 2),
            "data_points": len(prices),
            "latest_price": prices[0] if prices else None
        }
    
    @staticmethod
    async def forecast_price(asset_id: str, provider: str, days_ahead: int = 1):
        """Simple linear regression forecast"""
        db = MongoDB.get_db()
        data = list(db.timeseries.find(
            {"assetId": asset_id, "provider": provider},
            {"closePrice": 1, "timestamp": 1, "_id": 0}
        ).sort("timestamp", 1).limit(30))  # Last 30 days
        
        if len(data) < 3:
            return {"error": "Need at least 3 data points for forecast"}
        
        # Prepare data for regression
        X = np.array(range(len(data))).reshape(-1, 1)
        y = np.array([d['closePrice'] for d in data])
        
        # Train model
        model = LinearRegression()
        model.fit(X, y)
        
        # Forecast
        future_X = np.array([[len(data) + i] for i in range(days_ahead)])
        predictions = model.predict(future_X)
        
        return {
            "assetId": asset_id,
            "forecast_days": days_ahead,
            "predictions": [round(p, 2) for p in predictions],
            "confidence_score": round(model.score(X, y), 3),
            "trend": "up" if model.coef_[0] > 0 else "down"
        }
    
    @staticmethod
    async def price_volatility(asset_id: str, provider: str):
        """Calculate price volatility"""
        db = MongoDB.get_db()
        data = list(db.timeseries.find(
            {"assetId": asset_id, "provider": provider},
            {"closePrice": 1, "_id": 0}
        ).sort("timestamp", -1).limit(20))
        
        if len(data) < 2:
            return {"error": "Insufficient data"}
        
        prices = [d['closePrice'] for d in data]
        returns = np.diff(prices) / prices[:-1]
        volatility = np.std(returns) * np.sqrt(252)  # Annualized volatility
        
        return {
            "assetId": asset_id,
            "volatility": round(volatility, 4),
            "risk_level": "High" if volatility > 0.3 else ("Medium" if volatility > 0.15 else "Low"),
            "max_price": max(prices),
            "min_price": min(prices),
            "price_range": round(max(prices) - min(prices), 2)
        }
