from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field

class DataSource(BaseModel):
    """Data Provider/Vendor Model"""
    sourceId: str = Field(..., description="Unique source identifier")
    name: str = Field(..., description="Provider name (Nasdaq, Bloomberg, etc.)")
    baseUrl: str = Field(..., description="API base URL")
    apiType: str = Field(..., description="REST, WebSocket, etc.")
    authRequired: bool = False
    supportedAssets: list = Field(default_factory=list)
    validFrom: datetime = Field(default_factory=datetime.now)
    isValid: bool = True
    
class SourceResponse(BaseModel):
    sourceId: str
    name: str
    apiType: str
