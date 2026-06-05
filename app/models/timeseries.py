from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field

class TimeSeriesPoint(BaseModel):
    """Time Series Data Point Model"""
    dataPointId: str = Field(..., description="Unique identifier for this data point")
    assetId: str = Field(..., description="Reference to asset")
    provider: str = Field(..., description="Data provider/vendor")
    timestamp: datetime = Field(..., description="Date/time of this data point")
    
    # Common financial indicators
    openPrice: Optional[float] = None
    highPrice: Optional[float] = None
    lowPrice: Optional[float] = None
    closePrice: Optional[float] = None
    volume: Optional[float] = None
    adjustedClose: Optional[float] = None
    
    # Additional flexible attributes
    attributes: Dict[str, Any] = Field(default_factory=dict)
    
    # Provenance
    source: str = Field(..., description="API endpoint or file source")
    ingestedAt: datetime = Field(default_factory=datetime.now)
    
class TimeSeriesResponse(BaseModel):
    assetId: str
    provider: str
    data: list
