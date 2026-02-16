class BunnyException(Exception):
    """Base exception for all Bunny.net errors."""
    pass

class BunnyAuthError(BunnyException):
    """Raised when authentication fails (401)."""
    pass

class BunnyResourceNotFoundError(BunnyException):
    """Raised when a resource is not found (404)."""
    pass

class BunnyAPIError(BunnyException):
    """Raised when the API returns an error."""
    def __init__(self, message: str, status_code: int = None):
        super().__init__(message)
        self.status_code = status_code
