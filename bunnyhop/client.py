import httpx
from typing import Any, Dict, Optional

from .config import API_BASE_URL
from .resources.zone import ZoneResource
from .resources.storage import StorageResource

class BunnyClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = API_BASE_URL
        self._client = httpx.Client(
            base_url=self.base_url,
            headers={
                "AccessKey": self.api_key,
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            timeout=30.0
        )
        
        self.zone = ZoneResource(self)
        self.storage = StorageResource(self)

    def close(self):
        self._client.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def _request(
        self, 
        method: str, 
        endpoint: str, 
        json: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        data: Any = None
    ) -> Any:
        try:
            response = self._client.request(
                method=method, 
                url=endpoint, 
                json=json, 
                params=params, 
                content=data
            )
            response.raise_for_status()
            
            if response.status_code == 204:
                return None
                
            return response.json()
            
        except httpx.HTTPStatusError as e:
            status_code = e.response.status_code
            error_msg = f"HTTP Error {status_code}: {e.response.text}"
            
            if status_code == 401:
                raise BunnyAuthError("Invalid API Key or unauthorized access.")
            elif status_code == 404:
                raise BunnyResourceNotFoundError(f"Resource not found: {endpoint}")
            else:
                try:
                    error_data = e.response.json()
                    error_msg = error_data.get("Message", error_msg)
                except Exception:
                    pass
                raise BunnyAPIError(error_msg, status_code)
        except httpx.RequestError as e:
            raise BunnyAPIError(f"Request failed: {str(e)}")
