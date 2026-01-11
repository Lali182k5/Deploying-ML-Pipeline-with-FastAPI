# DataWise AI Delivery

## Step 1 → Architecture diagram (text)
```
User → FastAPI (API gateway)
        ├─ Schema Engine → Postgres (read-only) → ChromaDB (schema embeddings)
        ├─ NL → Intent Engine (LLM prompt + heuristics)
        ├─ SQL Generator → SQL Safety Engine → Postgres (parameterized)
        ├─ Data Quality Engine → Insight Engine
        ├─ Cache (Redis) ─┐
        ├─ History store ─┤
        └─ Celery workers ─┘ for async schema refresh / heavy queries
Frontend (Next.js + Socket.io) ↔ FastAPI for streaming results/insights
Artifacts: Chroma embeddings, query history, charts-ready JSON
```

## Step 2 → Database schema handling
- Reads PostgreSQL `information_schema` for tables/columns; falls back to bundled sample schema for offline runs.
- Stores table/column embeddings in ChromaDB (embedded path: `CHROMA_PATH`).
- Schema snapshots are cached and refreshed via Celery/background jobs to avoid hallucinating tables.

## Step 3 → Backend code
- FastAPI app exposes:
  - `GET /` health
  - `GET /schema` schema snapshot
  - `POST /query` NL → SQL pipeline
  - `GET /history` last queries
- Engines live in `backend/` (`schema_engine.py`, `intent_engine.py`, `sql_generator.py`, `sql_safety.py`, `data_quality.py`, `insight_engine.py`, `pipeline.py`, `executor.py`, `history.py`, `cache.py`).
- Safe execution path: intent → SQL → safety → execution → data quality → insights → history.

## Step 4 → AI pipeline
- NL → Intent Engine: extracts metrics/dimensions/filters/timeframes using schema awareness.
- SQL Generator: parameterized SELECT with enforced LIMIT; no writes.
- SQL Safety Engine: blocks writes/deletes, multi-statements, and over-limit queries.
- Execution: Postgres with psycopg if configured; otherwise sample data for local dev.
- Data Quality Engine: nulls, duplicates, freshness checks.
- Insight Engine: quick trends/top-entity summaries.

## Step 5 → Frontend
- Next.js 14 (React 18, Tailwind, shadcn/ui, Zustand) layout:
  - Chat-like query panel with streaming answers via Socket.io.
  - Results table (ag-grid/recharts-ready JSON from `/query`).
  - Chart view (line/bar based on returned columns).
  - “Why” button placeholder to surface insights and data quality notes.
- Deployment target: Vercel with `.env` pointing to FastAPI API URL.

## Step 6 → Deployment
- Backend: Dockerfile + `uvicorn main:app`. Deploy on Modal/Supabase functions with env vars `DATABASE_URL`, `REDIS_URL`, `CHROMA_PATH`.
- Celery/Redis: optional for async jobs; falls back to in-process background tasks.
- Frontend: `npm install && npm run build` then `vercel deploy`.

## Step 7 → How to extend later
- Swap heuristic intent with Ollama Llama 3.1 70B prompts; reuse schema embeddings for grounding.
- Add RBAC/auth (JWT) and row-level filters per user.
- Add async streaming for long queries; upgrade cache to managed Redis.
- Add full observability (OpenTelemetry traces, metrics, structured logs).
- Add CI with lint/tests and CodeQL.

