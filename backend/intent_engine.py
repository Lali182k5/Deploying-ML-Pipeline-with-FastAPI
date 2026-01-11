from __future__ import annotations

import re
from typing import Dict, List, Optional

from backend.models import NLIntent, SchemaSnapshot


class IntentEngine:
    """Converts natural language into structured intent."""

    @staticmethod
    def parse(question: str, schema: SchemaSnapshot, filters: Optional[Dict] = None) -> NLIntent:
        text = question.lower()
        filters = filters or {}
        table = IntentEngine._guess_table(text, schema)
        metrics: List[str] = []
        dimensions: List[str] = []

        if "revenue" in text or "amount" in text or "sales" in text:
            metrics.append("amount")
        if "orders" in text:
            metrics.append("order_count")
        if "customer" in text:
            dimensions.append("customer_id")
        if "country" in text:
            dimensions.append("country")
        if "segment" in text:
            dimensions.append("segment")
        timeframe = IntentEngine._extract_timeframe(text)

        confidence = 0.6 if table else 0.3
        if metrics:
            confidence += 0.1

        return NLIntent(
            metrics=metrics,
            dimensions=dimensions,
            filters=filters,
            timeframe=timeframe,
            table=table,
            confidence=min(confidence, 0.95),
        )

    @staticmethod
    def _guess_table(text: str, schema: SchemaSnapshot) -> Optional[str]:
        for table in schema.tables:
            if table in text:
                return table
        if "order" in text:
            return "orders" if "orders" in schema.tables else None
        if "customer" in text:
            return "customers" if "customers" in schema.tables else None
        return next(iter(schema.tables.keys()), None)

    @staticmethod
    def _extract_timeframe(text: str) -> Optional[str]:
        match = re.search(r"last (\d+)\s*(day|days|week|weeks|month|months)", text)
        if match:
            return f"last_{match.group(1)}_{match.group(2)}"
        if "today" in text:
            return "today"
        if "yesterday" in text:
            return "yesterday"
        return None

