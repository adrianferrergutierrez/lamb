# Evaluaitor — Development Log

Registro cronológico de cambios y progreso del microservicio Evaluaitor.

---

## 2026-02-17 — Phase 1: Foundation Skeleton

### Objetivo
Crear la estructura base del microservicio siguiendo los patrones de `lamb-kb-server-stable`.

### Ficheros creados (18 ficheros, 7 directorios)

| Fichero | Descripción |
|---------|-------------|
| `backend/main.py` | Entry point FastAPI: logging, startup event, routers, CORS, static files |
| `backend/config.py` | Configuración centralizada con variables de entorno y defaults |
| `backend/dependencies.py` | Autenticación Bearer token (patrón kb-server) |
| `backend/requirements.txt` | Dependencias: fastapi, uvicorn, sqlalchemy, httpx, pypdf, python-docx |
| `backend/.env.example` | Plantilla de variables de entorno |
| `backend/database/__init__.py` | Package init |
| `backend/database/models.py` | 4 modelos SQLAlchemy: `Organization`, `EvaluationJob`, `EvaluationResult`, `ExtractedContent` + enum `JobStatus` |
| `backend/database/connection.py` | Init SQLite, engine singleton, session factory, `get_db()` dependency |
| `backend/database/service.py` | CRUD: `OrganizationService`, `JobService`, `ResultService` |
| `backend/schemas/__init__.py` | Package init |
| `backend/schemas/system.py` | Pydantic: `HealthResponse`, `DatabaseStatusResponse` |
| `backend/schemas/organization.py` | Pydantic: `OrganizationCreate`, `OrganizationResponse`, `OrganizationDetailResponse` |
| `backend/schemas/evaluation.py` | Pydantic: `EvaluationSubmitResponse`, `EvaluationStatusResponse`, `EvaluationResultResponse`, etc. |
| `backend/routers/__init__.py` | Package init |
| `backend/routers/system.py` | `GET /health` (sin auth), `GET /database/status` (con auth) |
| `backend/routers/organizations.py` | `POST /organizations` (upsert), `GET /organizations/{external_id}` (con stats) |
| `backend/services/__init__.py` | Package init |
| `backend/services/lamb_client.py` | Cliente HTTP async para LAMB `/v1/chat/completions` (stub Phase 2) |
| `backend/extractors/__init__.py` | Placeholder Phase 2 |
| `backend/plugins/__init__.py` | Placeholder Phase 3 |

### Verificación

| Test | Resultado |
|------|-----------|
| Server arranca (port 9091) | ✅ |
| `GET /health` | ✅ `{"status":"ok","version":"0.1.0","service":"evaluaitor"}` |
| `GET /database/status` sin token | ✅ 401 Unauthorized |
| `GET /database/status` con token | ✅ 200 + stats BD |
| `POST /organizations` | ✅ 201 Created |
| `GET /organizations/test_org` | ✅ 200 + job stats |
| 4 tablas BD creadas al arrancar | ✅ `organizations`, `evaluation_jobs`, `evaluation_results`, `extracted_content` |
| Swagger UI en `/docs` | ✅ |

### Cómo ejecutar

```bash
cd evaluaitor/backend
source venv/bin/activate
EVALUAITOR_LOG_LEVEL=INFO uvicorn main:app --port 9091 --reload
```

---
