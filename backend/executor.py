from __future__ import annotations

from typing import Dict, Tuple

import pandas as pd

from backend import config
from backend.sample_data import CUSTOMERS, ORDERS

try:
    import psycopg
except ImportError:  # pragma: no cover - optional dependency
    psycopg = None


class QueryExecutor:
    """Executes validated SQL in a safe, read-only manner."""

    def __init__(self, settings: config.Settings):
        self.settings = settings

    def execute(self, sql: str, params: Dict) -> Tuple[pd.DataFrame, bool]:
        if psycopg and self.settings.database_url:
            with psycopg.connect(self.settings.database_url) as conn:
                with conn.cursor() as cur:
                    cur.execute(sql, params)
                    columns = [desc[0] for desc in cur.description]
                    rows = cur.fetchall()
                    df = pd.DataFrame(rows, columns=columns)
                    return df, False
        return self._execute_locally(sql)

    def _execute_locally(self, sql: str) -> Tuple[pd.DataFrame, bool]:
        """Simulated execution using sample data."""
        sql_lower = sql.lower()
        if "from orders" in sql_lower:
            df = ORDERS.copy()
            if "sum(amount)" in sql_lower or "total_amount" in sql_lower:
                df = (
                    df.groupby("customer_id")
                    .agg(total_amount=("amount", "sum"))
                    .reset_index()
                )
            if "count(*)" in sql_lower or "order_count" in sql_lower:
                counts = ORDERS.groupby("customer_id").agg(order_count=("order_id", "count"))
                df = counts.reset_index()
            return df, True
        if "from customers" in sql_lower:
            return CUSTOMERS.copy(), True
        return pd.DataFrame(), True

