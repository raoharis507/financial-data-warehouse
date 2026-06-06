import asyncio
from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
from mcp.types import Tool, TextContent, CallToolResult
import anyio
import httpx

# Create MCP Server instance
server = Server("financial-data-warehouse")

# Define available tools
@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    return [
        Tool(
            name="list_assets",
            description="List all financial assets in the warehouse",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="get_asset_details",
            description="Get detailed information about a specific asset",
            inputSchema={
                "type": "object",
                "properties": {
                    "asset_id": {"type": "string", "description": "Asset ID like AAPL, MSFT, BTC"}
                },
                "required": ["asset_id"]
            }
        ),
        Tool(
            name="get_time_series",
            description="Get time series data for an asset",
            inputSchema={
                "type": "object",
                "properties": {
                    "asset_id": {"type": "string", "description": "Asset ID"},
                    "provider": {"type": "string", "description": "Provider name like Nasdaq"},
                    "days": {"type": "integer", "description": "Number of days", "default": 5}
                },
                "required": ["asset_id", "provider"]
            }
        ),
        Tool(
            name="forecast_price",
            description="Forecast future prices using Spark ML",
            inputSchema={
                "type": "object",
                "properties": {
                    "asset_id": {"type": "string", "description": "Asset ID"},
                    "provider": {"type": "string", "description": "Provider name"},
                    "days_ahead": {"type": "integer", "description": "Days to forecast", "default": 3}
                },
                "required": ["asset_id", "provider"]
            }
        ),
        Tool(
            name="compare_assets",
            description="Compare two assets",
            inputSchema={
                "type": "object",
                "properties": {
                    "asset1": {"type": "string", "description": "First asset ID"},
                    "asset2": {"type": "string", "description": "Second asset ID"}
                },
                "required": ["asset1", "asset2"]
            }
        )
    ]

# Tool execution handlers
@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls from MCP client"""
    
    async with httpx.AsyncClient() as client:
        base_url = "http://127.0.0.1:8000"
        
        if name == "list_assets":
            response = await client.get(f"{base_url}/api/assets")
            data = response.json()
            result = f"Found {len(data)} assets: " + ", ".join([f"{a['assetId']} ({a['name']})" for a in data])
            
        elif name == "get_asset_details":
            asset_id = arguments.get("asset_id")
            response = await client.get(f"{base_url}/api/assets/{asset_id}")
            data = response.json()
            result = f"Asset {asset_id}: {data.get('name')} - Class: {data.get('assetClass')} - Region: {data.get('region')}"
            
        elif name == "get_time_series":
            asset_id = arguments.get("asset_id")
            provider = arguments.get("provider")
            response = await client.get(f"{base_url}/api/timeseries/{asset_id}/{provider}")
            data = response.json()
            prices = [f"${d['closePrice']}" for d in data.get('data', [])[:5]]
            result = f"Latest prices for {asset_id}: {', '.join(prices)}"
            
        elif name == "forecast_price":
            asset_id = arguments.get("asset_id")
            provider = arguments.get("provider")
            days_ahead = arguments.get("days_ahead", 3)
            response = await client.get(f"{base_url}/api/spark/forecast/{asset_id}/{provider}?days_ahead={days_ahead}")
            data = response.json()
            result = f"Forecast for {asset_id}: {data.get('predictions')} - Trend: {data.get('trend')} (using {data.get('engine')})"
            
        elif name == "compare_assets":
            asset1 = arguments.get("asset1")
            asset2 = arguments.get("asset2")
            # Use LLM assistant compare endpoint
            response = await client.get(f"{base_url}/api/assistant/ask?query=compare%20{asset1}%20and%20{asset2}")
            data = response.json()
            result = data.get("response")
            
        else:
            result = f"Unknown tool: {name}"
    
    return [TextContent(type="text", text=result)]


async def main():
    async with server.run_stdio():
        await anyio.sleep(float("inf"))

if __name__ == "__main__":
    anyio.run(main)
