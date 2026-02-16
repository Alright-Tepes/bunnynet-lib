from pydantic import BaseModel, Field
from typing import List, Optional

class Zone(BaseModel):
    id: Optional[int] = Field(None, alias="Id")
    name: str = Field(..., alias="Name")
    origin_url: str = Field(..., alias="OriginUrl")
    enabled: bool = Field(True, alias="Enabled")
    storage_zone_id: Optional[int] = Field(None, alias="StorageZoneId")
    allowed_referrers: List[str] = Field(default_factory=list, alias="AllowedReferrers")
    blocked_ips: List[str] = Field(default_factory=list, alias="BlockedIps")
    enable_cache_slice: bool = Field(False, alias="EnableCacheSlice")
    enable_geo_zone_us: bool = Field(False, alias="EnableGeoZoneUS")
    enable_geo_zone_eu: bool = Field(False, alias="EnableGeoZoneEU")
    enable_geo_zone_asia: bool = Field(False, alias="EnableGeoZoneASIA")
    enable_geo_zone_sa: bool = Field(False, alias="EnableGeoZoneSA")
    enable_geo_zone_af: bool = Field(False, alias="EnableGeoZoneAF")
    monthly_bandwidth_limit: int = Field(0, alias="MonthlyBandwidthLimit")
    
    # Add other fields as needed based on API docs or original lib
    # keeping it simple for now as requested
    
    class Config:
        populate_by_name = True
