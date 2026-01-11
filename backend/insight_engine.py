from __future__ import annotations

from typing import List

import pandas as pd

from backend.models import Insight


class InsightEngine:
    """Derive lightweight insights from aggregated query results."""

    def derive(self, df: pd.DataFrame) -> List[Insight]:
        insights: List[Insight] = []
        if df.empty:
            return insights

        if "total_amount" in df.columns and "customer_id" in df.columns:
            top = df.sort_values("total_amount", ascending=False).iloc[0]
            insights.append(
                Insight(
                    title="Top customer by revenue",
                    detail=f"Customer {top['customer_id']} leads with ${float(top['total_amount']):.2f} in sales.",
                    impact="positive",
                )
            )
        if "order_count" in df.columns:
            avg_orders = df["order_count"].mean()
            insights.append(
                Insight(
                    title="Average order volume",
                    detail=f"Average order count across groups: {avg_orders:.1f}",
                    impact="neutral",
                )
            )
        return insights

