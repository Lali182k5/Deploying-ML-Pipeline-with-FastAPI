from __future__ import annotations

from datetime import datetime, timezone
from typing import Dict, List

from backend import config
from backend.models import SchemaColumn, SchemaSnapshot

try:
    import psycopg
except ImportError:  # pragma: no cover - optional dependency
    psycopg = None


class SchemaEngine:
    """Reads and caches database schema to prevent hallucinated SQL."""

    def __init__(self, settings: config.Settings):
        self.settings = settings
        self._cache: SchemaSnapshot | None = None

    def load_schema(self) -> SchemaSnapshot:
        if self._cache:
            return self._cache

        if psycopg and self.settings.database_url:
            try:
                tables = self._fetch_from_db()
                snapshot = SchemaSnapshot(tables=tables, refreshed_at=datetime.now(timezone.utc))
                self._cache = snapshot
                return snapshot
            except Exception:
                pass  # fall back to sample schema

        sample_tables = {
            name: [
                SchemaColumn(
                    table=name,
                    name=col["name"],
                    data_type=col["data_type"],
                    nullable=col["nullable"],
                )
                for col in columns
            ]
            for name, columns in self.settings.sample_schema.items()
        }
        snapshot = SchemaSnapshot(tables=sample_tables, refreshed_at=datetime.now(timezone.utc))
        self._cache = snapshot
        return snapshot

    def _fetch_from_db(self) -> Dict[str, List[SchemaColumn]]:
        assert psycopg is not None
        tables: Dict[str, List[SchemaColumn]] = {}
        with psycopg.connect(self.settings.database_url) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT table_name, column_name, data_type, is_nullable
                    FROM information_schema.columns
                    WHERE table_schema='public'
                    ORDER BY table_name, ordinal_position
                    """
                )
                for table_name, column_name, data_type, is_nullable in cur.fetchall():
                    tables.setdefault(table_name, []).append(
                        SchemaColumn(
                            table=table_name,
                            name=column_name,
                            data_type=data_type,
                            nullable=is_nullable == "YES",
                        )
                    )
        return tables

    def refresh(self) -> SchemaSnapshot:
        self._cache = None
        return self.load_schema()
