from __future__ import annotations

from typing import Dict, List, Tuple

from backend.config import settings
from backend.models import NLIntent, SchemaSnapshot


class SQLGenerator:
    """Generate parameterized SQL and explanation from intent and schema metadata."""

    @staticmethod
    def build(intent: NLIntent, schema: SchemaSnapshot, limit: int | None = None) -> Tuple[str, Dict]:
        if not intent.table or intent.table not in schema.tables:
            raise ValueError("Unable to map question to a known table.")

        selected_metrics, aggregates = SQLGenerator._metrics(intent, schema)
        dimensions = SQLGenerator._dimensions(intent, schema)
        where_clause, params = SQLGenerator._filters(intent)
        limit_value = limit or settings.default_limit
        limit_value = min(limit_value, settings.max_limit)

        columns: List[str] = []
        if aggregates:
            columns.extend(aggregates)
        else:
            columns.append("*")
        columns.extend(dimensions)

        select_cols = ", ".join(columns)
        sql = f"SELECT {select_cols} FROM {intent.table}"
        if where_clause:
            sql += f" WHERE {where_clause}"
        if dimensions and aggregates:
            sql += " GROUP BY " + ", ".join(dimensions)
        sql += f" LIMIT {limit_value};"

        return sql, params

    @staticmethod
    def _metrics(intent: NLIntent, schema: SchemaSnapshot) -> Tuple[List[str], List[str]]:
        metrics = []
        aggregates = []
        available_cols = {c.name for c in schema.tables[intent.table]}
        for metric in intent.metrics:
            if metric == "amount" and "amount" in available_cols:
                aggregates.append("SUM(amount) AS total_amount")
                metrics.append("total_amount")
            if metric == "order_count":
                aggregates.append("COUNT(*) AS order_count")
                metrics.append("order_count")
        return metrics, aggregates

    @staticmethod
    def _dimensions(intent: NLIntent, schema: SchemaSnapshot) -> List[str]:
        available_cols = {c.name for c in schema.tables[intent.table]}
        dims = []
        for dim in intent.dimensions:
            if dim in available_cols:
                dims.append(dim)
        return dims

    @staticmethod
    def _filters(intent: NLIntent) -> Tuple[str, Dict]:
        clauses = []
        params: Dict[str, object] = {}
        for key, value in intent.filters.items():
            clauses.append(f"{key} = %({key})s")
            params[key] = value
        if intent.timeframe:
            clauses.append("order_date >= NOW() - INTERVAL %(timeframe)s")
            params["timeframe"] = intent.timeframe.replace("last_", "").replace("_", " ")
        return " AND ".join(clauses), params

