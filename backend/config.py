import os
from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class Settings:
    database_url: str | None = os.environ.get("DATABASE_URL")
    redis_url: str | None = os.environ.get("REDIS_URL")
    chroma_path: str = os.environ.get("CHROMA_PATH", "./.chroma")
    max_limit: int = int(os.environ.get("MAX_QUERY_LIMIT", "200"))
    default_limit: int = int(os.environ.get("DEFAULT_QUERY_LIMIT", "50"))
    cache_ttl_seconds: int = int(os.environ.get("CACHE_TTL_SECONDS", "300"))
    history_size: int = int(os.environ.get("HISTORY_SIZE", "50"))
    sample_schema: Dict[str, List[Dict[str, str]]] = field(
        default_factory=lambda: {
            "orders": [
                {"name": "order_id", "data_type": "int", "nullable": False},
                {"name": "customer_id", "data_type": "int", "nullable": False},
                {"name": "order_date", "data_type": "timestamp", "nullable": False},
                {"name": "status", "data_type": "text", "nullable": False},
                {"name": "amount", "data_type": "numeric", "nullable": False},
                {"name": "channel", "data_type": "text", "nullable": True},
            ],
            "customers": [
                {"name": "customer_id", "data_type": "int", "nullable": False},
                {"name": "segment", "data_type": "text", "nullable": True},
                {"name": "country", "data_type": "text", "nullable": True},
                {"name": "created_at", "data_type": "timestamp", "nullable": False},
            ],
        }
    )


settings = Settings()

