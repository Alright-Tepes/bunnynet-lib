from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class StorageZone(BaseModel):
    id: Optional[int] = Field(None, alias="Id")
    name: str = Field(..., alias="Name")
    password: Optional[str] = Field(None, alias="Password")
    read_only_password: Optional[str] = Field(None, alias="ReadOnlyPassword")
    region: str = Field("DE", alias="Region")
    replication_regions: List[str] = Field(default_factory=list, alias="ReplicationRegions")
    date_modified: Optional[datetime] = Field(None, alias="DateModified")
    deleted: bool = Field(False, alias="Deleted")
    storage_used: Optional[int] = Field(None, alias="StorageUsed")
    files_stored: Optional[int] = Field(None, alias="FilesStored")
    
    class Config:
        populate_by_name = True
