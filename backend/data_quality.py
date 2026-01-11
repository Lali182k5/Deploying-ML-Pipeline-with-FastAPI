from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import List

import pandas as pd

from backend.models import DataQualityFinding


class DataQualityEngine:
    """Run lightweight data quality checks on query output."""

    def evaluate(self, df: pd.DataFrame) -> List[DataQualityFinding]:
        findings: List[DataQualityFinding] = []
        if df.empty:
            findings.append(
                DataQualityFinding(
                    type="emptiness",
                    message="Query returned no rows.",
                    severity="warning",
                )
            )
            return findings

        null_share = df.isnull().mean().max()
        if null_share > 0.3:
            findings.append(
                DataQualityFinding(
                    type="nulls",
                    message=f"High null rate detected (max column null share {null_share:.0%}).",
                    severity="warning",
                )
            )

        duplicate_ratio = (len(df) - len(df.drop_duplicates())) / max(len(df), 1)
        if duplicate_ratio > 0.1:
            findings.append(
                DataQualityFinding(
                    type="duplicates",
                    message="Potential duplicate rows detected.",
                    severity="warning",
                )
            )

        if "order_date" in df.columns:
            try:
                df_dates = pd.to_datetime(df["order_date"], utc=True)
                max_date = df_dates.max().to_pydatetime()
                if datetime.now(timezone.utc) - max_date > timedelta(days=60):
                    findings.append(
                        DataQualityFinding(
                            type="freshness",
                            message="Data may be stale (older than 60 days).",
                            severity="warning",
                        )
                    )
            except Exception:
                pass

        return findings
