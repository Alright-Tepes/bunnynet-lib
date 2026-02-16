from typing import List, Optional, Any, TYPE_CHECKING
import httpx
from ..models.storage import StorageZone
from ..config import STORAGE_BASE_URL_TEMPLATE
from ..exceptions import BunnyAPIError, BunnyAuthError, BunnyResourceNotFoundError

if TYPE_CHECKING:
    from ..client import BunnyClient

class StorageResource:
    def __init__(self, client: "BunnyClient"):
        self.client = client

    def list(self) -> List[StorageZone]:
        """List all Storage Zones."""
        data = self.client._request("GET", "/storagezone")
        return [StorageZone(**item) for item in data]

    def create(self, name: str, region: str = "DE", replication_regions: List[str] = None) -> StorageZone:
        """Create a new Storage Zone."""
        payload = {
            "Name": name,
            "Region": region,
            "ReplicationRegions": replication_regions or []
        }
        data = self.client._request("POST", "/storagezone", json=payload)
        return StorageZone(**data)

    def delete(self, zone_id: int) -> bool:
        """Delete a Storage Zone."""
        self.client._request("DELETE", f"/storagezone/{zone_id}")
        return True

    def get(self, zone_id: int) -> StorageZone:
        """Get a single Storage Zone."""
        data = self.client._request("GET", f"/storagezone/{zone_id}")
        return StorageZone(**data)

    # File Operations
    
    def _get_storage_client(self, region: str) -> httpx.Client:
        base_url = STORAGE_BASE_URL_TEMPLATE.format(region=region)
        return httpx.Client(base_url=base_url, timeout=60.0)

    def upload_file(self, zone: StorageZone, path: str, file_content: bytes, filename: str) -> bool:
        """
        Upload a file to a Storage Zone.
        path: Directory path (e.g. 'images/')
        filename: Name of the file (e.g. 'logo.png')
        """
        if not zone.password:
            raise ValueError("StorageZone object must have a Password to upload files.")
            
        region = zone.region.lower() if zone.region else "de"
        # Edge case: Main region might be different, but let's assume standard behavior for now.
        
        url_path = f"/{zone.name}/{path}/{filename}".replace("//", "/")
        
        headers = {
            "AccessKey": zone.password,
            "Content-Type": "application/octet-stream"
        }
        
        with self._get_storage_client(region) as client:
            response = client.put(url_path, content=file_content, headers=headers)
            
            if response.status_code == 201:
                return True
            
            if response.status_code != 200:
                 raise BunnyAPIError(f"Upload failed: {response.text}", response.status_code)
                 
            return True

    def download_file(self, zone: StorageZone, path: str, filename: str) -> bytes:
        """Download a file from a Storage Zone."""
        if not zone.password:
             raise ValueError("StorageZone object must have a Password.")

        region = zone.region.lower() if zone.region else "de"
        url_path = f"/{zone.name}/{path}/{filename}".replace("//", "/")
        
        headers = {"AccessKey": zone.password}
        
        with self._get_storage_client(region) as client:
            response = client.get(url_path, headers=headers)
            
            if response.status_code == 404:
                raise BunnyResourceNotFoundError(f"File not found: {filename}")
            
            if response.status_code != 200:
                raise BunnyAPIError(f"Download failed: {response.text}", response.status_code)
                
            return response.content

    def delete_file(self, zone: StorageZone, path: str, filename: str) -> bool:
        """Delete a file from a Storage Zone."""
        if not zone.password:
             raise ValueError("StorageZone object must have a Password.")

        region = zone.region.lower() if zone.region else "de"
        url_path = f"/{zone.name}/{path}/{filename}".replace("//", "/")
        
        headers = {"AccessKey": zone.password}
        
        with self._get_storage_client(region) as client:
            response = client.delete(url_path, headers=headers)
            
            if response.status_code == 200:
                return True
            if response.status_code == 404:
                raise BunnyResourceNotFoundError(f"File not found: {filename}")
                
            raise BunnyAPIError(f"Delete failed: {response.text}", response.status_code)
