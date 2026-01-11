from __future__ import annotations

from datetime import datetime, timezone
from hashlib import sha256
from typing import Dict, Tuple

import pandas as pd

from backend.cache import TTLCache
from backend.config import settings
from backend.data_quality import DataQualityEngine
from backend.executor import QueryExecutor
from backend.history import HistoryStore
from backend.insight_engine import InsightEngine
from backend.intent_engine import IntentEngine
from backend.models import (
    HistoryItem,
    QueryRequest,
    QueryResponse,
    QueryResult,
)
from backend.schema_engine import SchemaEngine
from backend.sql_generator import SQLGenerator
from backend.sql_safety import SQLSafetyEngine


class DataWisePipeline:
    """End-to-end orchestration from NL to safe SQL and insights."""

    def __init__(
        self,
        schema_engine: SchemaEngine,
        executor: QueryExecutor,
        cache: TTLCache,
        history: HistoryStore,
    ):
        self.schema_engine = schema_engine
        self.intent_engine = IntentEngine()
        self.executor = executor
        self.quality_engine = DataQualityEngine()
        self.insight_engine = InsightEngine()
        self.cache = cache
        self.history = history

    def run(self, request: QueryRequest) -> QueryResponse:
        schema = self.schema_engine.load_schema()
        intent = self.intent_engine.parse(request.question, schema, request.filters)
        sql, params = SQLGenerator.build(intent, schema, request.limit)
        SQLSafetyEngine.validate(sql, params)

        cache_key = self._cache_key(request.question, params)
        cached = self.cache.get(cache_key)
        if cached:
            return cached

        df, simulated = self.executor.execute(sql, params)
        data_quality = self.quality_engine.evaluate(df)
        insights = self.insight_engine.derive(df)
        response = QueryResponse(
            sql=sql,
            parameters=params,
            confidence=intent.confidence,
            data_quality=data_quality,
            explanation=self._build_explanation(intent),
            insights=insights,
            result=QueryResult(columns=list(df.columns), rows=df.values.tolist()),
            cached=False,
            executed_at=datetime.now(timezone.utc),
        )
        self.cache.set(cache_key, response.model_copy(update={"cached": True}))
        self.history.add(
            HistoryItem(
                question=request.question,
                sql=sql,
                executed_at=response.executed_at,
                rowcount=len(df),
                warnings=[f.type for f in data_quality if f.severity != "info"],
            )
        )
        return response

    @staticmethod
    def _cache_key(question: str, params: Dict) -> str:
        payload = f"{question}|{sorted(params.items())}"
        return sha256(payload.encode()).hexdigest()

    @staticmethod
    def _build_explanation(intent) -> str:
        parts = [
            f"Target table: {intent.table}",
            f"Metrics: {', '.join(intent.metrics) or 'none'}",
            f"Dimensions: {', '.join(intent.dimensions) or 'none'}",
        ]
        if intent.timeframe:
            parts.append(f"Timeframe: {intent.timeframe}")
        if intent.filters:
            parts.append(f"Filters: {intent.filters}")
        return "; ".join(parts)
