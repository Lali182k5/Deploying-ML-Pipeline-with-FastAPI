from __future__ import annotations

from collections import deque
from typing import Deque, List

from backend.config import settings
from backend.models import HistoryItem


class HistoryStore:
    """Keeps recent query history for transparency."""

    def __init__(self, capacity: int = settings.history_size):
        self.capacity = capacity
        self._items: Deque[HistoryItem] = deque(maxlen=capacity)

    def add(self, item: HistoryItem) -> None:
        self._items.appendleft(item)

    def list(self) -> List[HistoryItem]:
        return list(self._items)

