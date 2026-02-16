from typing import List, Optional, Any, TYPE_CHECKING
from ..models.zone import Zone

if TYPE_CHECKING:
    from ..client import BunnyClient

class ZoneResource:
    def __init__(self, client: "BunnyClient"):
        self.client = client

    def get(self, zone_id: int) -> Zone:
        """Get a single Pull Zone by ID."""
        data = self.client._request("GET", f"/pullzone/{zone_id}")
        return Zone(**data)

    def list(self) -> List[Zone]:
        """List all Pull Zones."""
        data = self.client._request("GET", "/pullzone")
        return [Zone(**item) for item in data]

    def create(self, name: str, origin_url: str, **kwargs) -> Zone:
        """Create a new Pull Zone."""
        payload = {
            "Name": name,
            "OriginUrl": origin_url,
            **kwargs
        }
        data = self.client._request("POST", "/pullzone", json=payload)
        return Zone(**data)

    def delete(self, zone_id: int) -> bool:
        """Delete a Pull Zone."""
        self.client._request("DELETE", f"/pullzone/{zone_id}")
        return True

    def purge(self, zone_id: int) -> bool:
        """Purge the cache for a Pull Zone."""
        self.client._request("POST", f"/pullzone/{zone_id}/purgeCache")
        return True
