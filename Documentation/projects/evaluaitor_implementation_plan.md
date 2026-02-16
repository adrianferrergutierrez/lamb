# Evaluaitor Microservice — Phase 1 Foundation Skeleton

Create the foundational project structure for the Evaluaitor microservice, following the architectural patterns of [lamb-kb-server-stable](file:///home/adrif/lamb/lamb-kb-server-stable/backend) as specified in the [project proposal](file:///home/adrif/lamb/Documentation/projects/lamb-evaluaitor-project.md).

> [!IMPORTANT]
> This creates a **new directory** `evaluaitor/` at the project root (`/home/adrif/lamb/evaluaitor/`). No existing code is modified.

## Proposed Changes

### Project Structure

The new directory tree:

```
evaluaitor/
└── backend/
    ├── main.py                  # FastAPI app + startup + CORS + logging
    ├── config.py                # Environment variable management
    ├── dependencies.py          # Bearer token authentication
    ├── requirements.txt         # Python dependencies
    ├── .env.example             # Environment template
    │
    ├── database/
    │   ├── __init__.py
    │   ├── connection.py        # SQLite init + session management
    │   ├── models.py            # SQLAlchemy ORM: organizations, jobs, results, extracted_content
    │   └── service.py           # Database CRUD operations
    │
    ├── routers/
    │   ├── __init__.py
    │   ├── system.py            # GET /health, GET /database/status
    │   └── organizations.py     # POST/GET /organizations
    │
    ├── services/
    │   ├── __init__.py
    │   └── lamb_client.py       # LAMB API client (stub for Phase 2)
    │
    ├── schemas/
    │   ├── __init__.py
    │   ├── system.py            # HealthResponse, DatabaseStatus
    │   ├── organization.py      # OrganizationCreate, OrganizationResponse
    │   └── evaluation.py        # EvaluationSubmit, JobStatus enum, etc.
    │
    ├── extractors/
    │   └── __init__.py          # Placeholder for Phase 2
    │
    ├── plugins/
    │   └── __init__.py          # Placeholder for Phase 3
    │
    ├── static/                  # Upload directory (created at startup)
    └── data/                    # Database directory (created at startup)
```

---

### Core Files

#### [NEW] [main.py](file:///home/adrif/lamb/evaluaitor/backend/main.py)
FastAPI application entry point. Follows [kb-server main.py](file:///home/adrif/lamb/lamb-kb-server-stable/backend/main.py) pattern:
- Logging config from `EVALUAITOR_LOG_LEVEL` / `GLOBAL_LOG_LEVEL`
- `.env` loading via `python-dotenv`
- Startup event: init database, ensure directories
- Include routers (system, organizations)
- CORS middleware (allow all origins)
- Static files mount

#### [NEW] [config.py](file:///home/adrif/lamb/evaluaitor/backend/config.py)
Environment configuration following [kb-server config.py](file:///home/adrif/lamb/lamb-kb-server-stable/backend/config.py):
- `EVALUAITOR_API_KEY` (default: `0p3n-w3bu!`)
- `LAMB_API_URL` (default: `http://localhost:9099`)
- `LAMB_TIMEOUT` (default: `120`)
- `DATABASE_PATH` (default: `data/evaluaitor.db`)
- `STATIC_PATH` (default: `static`)
- `MAX_FILE_SIZE_MB` (default: `100`)

#### [NEW] [dependencies.py](file:///home/adrif/lamb/evaluaitor/backend/dependencies.py)
Bearer token auth, identical pattern to [kb-server dependencies.py](file:///home/adrif/lamb/lamb-kb-server-stable/backend/dependencies.py):
- `HTTPBearer` security scheme
- `verify_token()` dependency comparing against `EVALUAITOR_API_KEY`

#### [NEW] [requirements.txt](file:///home/adrif/lamb/evaluaitor/backend/requirements.txt)
Minimal dependencies for Phase 1:
- `fastapi`, `uvicorn`, `pydantic`, `python-dotenv`
- `sqlalchemy` (database ORM)
- `python-multipart` (file uploads in Phase 2)
- `httpx` (async HTTP client for LAMB API)
- `pypdf` (PDF extraction in Phase 2)
- `python-docx` (DOCX extraction in Phase 2)

---

### Database Layer

#### [NEW] [database/models.py](file:///home/adrif/lamb/evaluaitor/backend/database/models.py)
SQLAlchemy ORM models matching the schema from Section 4.1 of the project proposal:
- `Organization` — synced from LAMB (`external_id`, `name`, `config`)
- `EvaluationJob` — job tracking (`job_code`, `evaluator_id`, `status`, `plugin_name`, file info, progress, timing)
- `EvaluationResult` — evaluation output (`score`, `score_normalized`, `feedback`, `raw_response`)
- `ExtractedContent` — cached extracted text (`content_text`, `extraction_method`, metadata)
- `JobStatus` enum: `pending`, `processing`, `completed`, `failed`, `cancelled`

#### [NEW] [database/connection.py](file:///home/adrif/lamb/evaluaitor/backend/database/connection.py)
SQLite database initialization and session management:
- `init_database()` — creates tables, ensures data directory exists
- `get_db()` — FastAPI dependency yielding SQLAlchemy sessions
- `get_engine()` — singleton engine access

#### [NEW] [database/service.py](file:///home/adrif/lamb/evaluaitor/backend/database/service.py)
Low-level CRUD operations:
- `create_organization()`, `get_organization_by_external_id()`
- `create_job()`, `get_job_by_code()`, `update_job_status()`
- `create_result()`, `get_result_by_job_id()`

---

### Routers & Schemas

#### [NEW] [routers/system.py](file:///home/adrif/lamb/evaluaitor/backend/routers/system.py)
- `GET /health` — no auth, returns `{"status": "ok", "version": "0.1.0", "service": "evaluaitor"}`
- `GET /database/status` — requires auth, returns DB stats (jobs count, pending, orgs count)

#### [NEW] [routers/organizations.py](file:///home/adrif/lamb/evaluaitor/backend/routers/organizations.py)
- `POST /organizations` — register/upsert organization
- `GET /organizations/{external_id}` — get org with job stats

#### [NEW] [schemas/system.py](file:///home/adrif/lamb/evaluaitor/backend/schemas/system.py)
Pydantic models: `HealthResponse`, `DatabaseStatusResponse`

#### [NEW] [schemas/organization.py](file:///home/adrif/lamb/evaluaitor/backend/schemas/organization.py)
Pydantic models: `OrganizationCreate`, `OrganizationResponse`

#### [NEW] [schemas/evaluation.py](file:///home/adrif/lamb/evaluaitor/backend/schemas/evaluation.py)
Pydantic models (stubs for Phase 2): `EvaluationSubmit`, `EvaluationStatusResponse`, `EvaluationResultResponse`

---

## Verification Plan

### Automated Tests

```bash
# 1. Start the server
cd /home/adrif/lamb/evaluaitor/backend
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 9091 --reload
```

```bash
# 2. Test health endpoint (no auth)
curl http://localhost:9091/health
# Expected: {"status":"ok","version":"0.1.0","service":"evaluaitor"}

# 3. Test auth rejection
curl http://localhost:9091/database/status
# Expected: 403 Forbidden (no token)

# 4. Test auth acceptance
curl -H "Authorization: Bearer 0p3n-w3bu!" http://localhost:9091/database/status
# Expected: 200 with {"sqlite_status":{"initialized":true},...}

# 5. Create organization
curl -X POST http://localhost:9091/organizations \
  -H "Authorization: Bearer 0p3n-w3bu!" \
  -H "Content-Type: application/json" \
  -d '{"external_id":"test_org","name":"Test University"}'
# Expected: 201 Created with organization data

# 6. Get organization
curl -H "Authorization: Bearer 0p3n-w3bu!" http://localhost:9091/organizations/test_org
# Expected: 200 with organization data including job stats

# 7. Verify database file created
ls -la /home/adrif/lamb/evaluaitor/backend/data/evaluaitor.db
# Expected: file exists
```

### Manual Verification
- Open `http://localhost:9091/docs` in browser → Swagger UI should load with all endpoints documented
- Verify no import errors in terminal output on startup
