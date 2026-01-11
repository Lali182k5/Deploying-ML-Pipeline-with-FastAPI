import re
from typing import Dict

from backend.config import settings


class SQLSafetyEngine:
    """Validate SQL for read-only, safe execution."""

    DISALLOWED = {"insert", "update", "delete", "drop", "alter", "truncate"}

    @staticmethod
    def validate(sql: str, params: Dict) -> None:
        lowered = sql.lower()
        if not lowered.strip().startswith("select"):
            raise ValueError("Only read-only SELECT queries are permitted.")
        if any(word in lowered for word in SQLSafetyEngine.DISALLOWED):
            raise ValueError("Write operations are blocked by safety policy.")
        limit_match = re.search(r"limit\s+(\d+)", lowered)
        if limit_match and int(limit_match.group(1)) > settings.max_limit:
            raise ValueError("Query limit exceeds allowed maximum.")
        if ";" in lowered[:-1]:
            raise ValueError("Multiple statements are not allowed.")
        for key in params:
            if ";" in str(params[key]):
                raise ValueError("Potential injection attempt detected in parameters.")

