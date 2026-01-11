import time
from typing import Any, Dict, Tuple

from backend.config import settings


class TTLCache:
    """Lightweight in-memory cache to mimic Redis for local runs."""

    def __init__(self, ttl_seconds: int = settings.cache_ttl_seconds):
        self.ttl = ttl_seconds
        self._data: Dict[str, Tuple[float, Any]] = {}

    def get(self, key: str) -> Any | None:
        if key not in self._data:
            return None
        expires_at, value = self._data[key]
        if time.time() > expires_at:
            del self._data[key]
            return None
        return value

    def set(self, key: str, value: Any) -> None:
        self._data[key] = (time.time() + self.ttl, value)

