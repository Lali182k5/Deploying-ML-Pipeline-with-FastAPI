from fastapi import Depends, FastAPI, HTTPException

from backend.cache import TTLCache
from backend.config import settings
from backend.executor import QueryExecutor
from backend.history import HistoryStore
from backend.models import QueryRequest
from backend.pipeline import DataWisePipeline
from backend.schema_engine import SchemaEngine

_pipeline = DataWisePipeline(
    SchemaEngine(settings),
    QueryExecutor(settings),
    TTLCache(),
    HistoryStore(),
)


def get_pipeline():
    return _pipeline


pipeline_dependency = Depends(get_pipeline)


def create_app() -> FastAPI:
    app = FastAPI(title="DataWise AI", version="0.1.0")

    @app.get("/")
    def health():
        return {"message": "DataWise AI is ready. Use /query to ask questions."}

    @app.get("/schema")
    def schema(pipeline: DataWisePipeline = pipeline_dependency):
        snapshot = pipeline.schema_engine.load_schema()
        return snapshot

    @app.post("/query")
    def query(request: QueryRequest, pipeline: DataWisePipeline = pipeline_dependency):
        try:
            response = pipeline.run(request)
            return response
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.get("/history")
    def history(pipeline: DataWisePipeline = pipeline_dependency):
        return pipeline.history.list()

    return app
