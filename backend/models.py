from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class SchemaColumn(BaseModel):
    table: str
    name: str
    data_type: str
    nullable: bool = False
    description: Optional[str] = None


class SchemaSnapshot(BaseModel):
    tables: Dict[str, List[SchemaColumn]]
    refreshed_at: datetime


class NLIntent(BaseModel):
    metrics: List[str] = Field(default_factory=list)
    dimensions: List[str] = Field(default_factory=list)
    filters: Dict[str, Any] = Field(default_factory=dict)
    timeframe: Optional[str] = None
    table: Optional[str] = None
    confidence: float = 0.5


class QueryRequest(BaseModel):
    question: str
    filters: Dict[str, Any] = Field(default_factory=dict)
    user_id: Optional[str] = None
    limit: Optional[int] = None


class DataQualityFinding(BaseModel):
    type: str
    message: str
    severity: str = "info"


class Insight(BaseModel):
    title: str
    detail: str
    impact: str = "neutral"


class QueryResult(BaseModel):
    columns: List[str]
    rows: List[List[Any]]


class QueryResponse(BaseModel):
    sql: str
    parameters: Dict[str, Any] = Field(default_factory=dict)
    confidence: float
    data_quality: List[DataQualityFinding] = Field(default_factory=list)
    explanation: str
    insights: List[Insight] = Field(default_factory=list)
    result: QueryResult
    cached: bool = False
    executed_at: datetime


class HistoryItem(BaseModel):
    question: str
    sql: str
    executed_at: datetime
    rowcount: int
    warnings: List[str] = Field(default_factory=list)

