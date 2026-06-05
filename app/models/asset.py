from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field

class Asset(BaseModel):
    """Financial Asset Model"""
    assetId: str = Field(..., description="Unique asset identifier")
    symbol: str = Field(..., description="Trading symbol (e.g., AAPL, BTC)")
    name: str = Field(..., description="Full name of the asset")
    assetClass: str = Field(..., description="stock, bond, crypto, etc.")
    region: str = Field(..., description="US, Europe, China, etc.")
    description: Optional[str] = None
    provider: str = Field(..., description="Data source/provider")
    validFrom: datetime = Field(default_factory=datetime.now)
    validTo: Optional[datetime] = None
    isDeleted: bool = False
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
class AssetResponse(BaseModel):
    assetId: str
    symbol: str
    name: str
    assetClass: str
    region: str
    
class AssetDetailResponse(AssetResponse):
    description: Optional[str]
    provider: str
    validFrom: datetime
    metadata: Dict[str, Any]
