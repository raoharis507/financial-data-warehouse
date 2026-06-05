import json
from datetime import datetime
from app.database.mongodb import MongoDB
from app.services.analytics import AnalyticsService

class LLMAssistant:
    """LLM-powered assistant for natural language queries"""
    
    @staticmethod
    async def process_query(query: str):
        """Process natural language query and return response"""
        query_lower = query.lower()
        
        # Tool 1: List assets
        if "list assets" in query_lower or "show assets" in query_lower:
            db = MongoDB.get_db()
            assets = list(db.assets.find({"isDeleted": False}, {"_id": 0, "assetId": 1, "name": 1, "assetClass": 1}))
            return {
                "query": query,
                "tool_used": "list_assets",
                "response": f"I found {len(assets)} assets: " + ", ".join([f"{a['assetId']} ({a['name']})" for a in assets]),
                "data": assets
            }
        
        # Tool 2: Fetch time series
        elif "time series" in query_lower or "prices" in query_lower:
            words = query_lower.split()
            asset = None
            for w in words:
                if w.upper() in ["AAPL", "MSFT", "BTC"]:
                    asset = w.upper()
                    break
            
            if asset:
                db = MongoDB.get_db()
                data = list(db.timeseries.find(
                    {"assetId": asset},
                    {"_id": 0, "timestamp": 1, "closePrice": 1}
                ).sort("timestamp", -1).limit(5))
                
                price_str = ", ".join([f"${d['closePrice']} on {d['timestamp'].strftime('%Y-%m-%d')}" for d in data])
                return {
                    "query": query,
                    "tool_used": "fetch_timeseries",
                    "response": f"Here are the latest prices for {asset}: {price_str}",
                    "data": data
                }
            else:
                return {
                    "query": query,
                    "tool_used": "fetch_timeseries", 
                    "response": "Which asset would you like to see? Try AAPL, MSFT, or BTC"
                }
        
        # Tool 3: Summarize trends
        elif "trend" in query_lower or "summarize" in query_lower:
            db = MongoDB.get_db()
            assets = list(db.assets.find({"isDeleted": False}, {"assetId": 1}))
            trends = []
            for asset in assets[:3]:
                ma = await AnalyticsService.calculate_moving_average(asset["assetId"], "Nasdaq", 5)
                if "moving_average" in ma:
                    trends.append(f"{asset['assetId']}: 5-day MA = ${ma['moving_average']}")
            
            return {
                "query": query,
                "tool_used": "summarize_trends",
                "response": "Trend summary:\n" + "\n".join(trends),
                "data": trends
            }
        
        # Tool 4: Compare two assets
        elif "compare" in query_lower:
            import re
            # Find asset symbols in the query
            symbols = re.findall(r'\b(AAPL|MSFT|BTC)\b', query.upper())
            unique_symbols = list(set(symbols))
            
            if len(unique_symbols) >= 2:
                asset1, asset2 = unique_symbols[0], unique_symbols[1]
                vol1 = await AnalyticsService.price_volatility(asset1, "Nasdaq")
                vol2 = await AnalyticsService.price_volatility(asset2, "Nasdaq")
                
                vol1_pct = vol1.get('volatility', 0) * 100
                vol2_pct = vol2.get('volatility', 0) * 100
                
                return {
                    "query": query,
                    "tool_used": "compare_assets",
                    "response": f"Comparison: {asset1} volatility = {vol1_pct:.1f}% ({vol1.get('risk_level', 'N/A')} risk), {asset2} volatility = {vol2_pct:.1f}% ({vol2.get('risk_level', 'N/A')} risk). {asset1} price range: ${vol1.get('min_price',0)} - ${vol1.get('max_price',0)}, {asset2} price range: ${vol2.get('min_price',0)} - ${vol2.get('max_price',0)}.",
                    "data": {"asset1": vol1, "asset2": vol2}
                }
            else:
                return {
                    "query": query,
                    "tool_used": "compare_assets", 
                    "response": "Please specify two assets to compare. Example: 'compare AAPL and MSFT'"
                }
        
        # Default response
        else:
            return {
                "query": query,
                "tool_used": "none",
                "response": "I can help with:\n- 'list assets' (show all assets)\n- 'show time series for AAPL' (get price history)\n- 'summarize trends' (show moving averages)\n- 'compare AAPL and MSFT' (compare volatility and risk)"
            }
