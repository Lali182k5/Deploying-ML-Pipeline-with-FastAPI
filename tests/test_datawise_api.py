import sys
from pathlib import Path

from fastapi.testclient import TestClient

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from backend.api import create_app

app = create_app()

client = TestClient(app)


def test_schema_endpoint():
    response = client.get("/schema")
    assert response.status_code == 200
    body = response.json()
    assert "tables" in body
    assert body["tables"]


def test_query_endpoint_returns_sql_and_explanation():
    payload = {"question": "Show revenue by customer", "filters": {}, "limit": 5}
    response = client.post("/query", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["sql"].lower().startswith("select")
    assert "explanation" in body
    assert "result" in body and "rows" in body["result"]
    assert "data_quality" in body
    assert "confidence" in body


def test_history_collects_previous_queries():
    client.post("/query", json={"question": "orders by customer", "filters": {}})
    hist = client.get("/history")
    assert hist.status_code == 200
    assert isinstance(hist.json(), list)
    assert len(hist.json()) >= 1
