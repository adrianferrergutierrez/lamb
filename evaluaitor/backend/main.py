"""
Evaluaitor — AI-Powered Evaluation Microservice.

Main FastAPI application entry point.
Part of the LAMB ecosystem (https://github.com/Lamb-Project/lamb).
"""

import os
import sys
import logging

# ═══════════════════════════════════════════════════════════════
# Logging Configuration
# ═══════════════════════════════════════════════════════════════

_LOG_LEVELS = {"CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"}
_effective_level = os.getenv(
    "EVALUAITOR_LOG_LEVEL",
    os.getenv("GLOBAL_LOG_LEVEL", "WARNING"),
).upper().strip()
if _effective_level not in _LOG_LEVELS:
    _effective_level = "WARNING"

logging.basicConfig(
    stream=sys.stdout,
    level=getattr(logging, _effective_level),
    format="%(levelname)s: %(name)s: %(message)s",
    force=True,
)
logger = logging.getLogger("evaluaitor")

# ═══════════════════════════════════════════════════════════════
# Environment Variables
# ═══════════════════════════════════════════════════════════════

try:
    from dotenv import load_dotenv
    load_dotenv()
    logger.debug("Environment variables loaded from .env file")
except ImportError:
    logger.warning("python-dotenv not installed; environment variables must be set manually")

# ═══════════════════════════════════════════════════════════════
# FastAPI Application
# ═══════════════════════════════════════════════════════════════

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from config import SERVICE_VERSION, STATIC_PATH, ensure_directories
from database.connection import init_database

app = FastAPI(
    title="LAMB Evaluaitor",
    description="""AI-Powered Evaluation Microservice for the LAMB ecosystem.

Evaluaitor provides automated evaluation of student submissions using
LAMB's AI assistants. It supports rubric-based evaluation through a
plugin architecture and processes jobs asynchronously.

## Authentication

All API endpoints (except `/health`) are secured with Bearer token authentication.

```
curl -H 'Authorization: Bearer YOUR_TOKEN' http://localhost:9091/database/status
```

## Key Features

- **Async Job Processing** — Submit evaluations and poll for results
- **Multi-Tenancy** — Organization-scoped data isolation
- **Plugin Architecture** — Extensible evaluation strategies
- **Document Extraction** — PDF, DOCX, TXT, and code files
""",
    version=SERVICE_VERSION,
    contact={
        "name": "LAMB Project Team",
    },
    license_info={
        "name": "GNU General Public License v3.0",
        "url": "https://www.gnu.org/licenses/gpl-3.0.en.html",
    },
)


# ═══════════════════════════════════════════════════════════════
# Startup
# ═══════════════════════════════════════════════════════════════

@app.on_event("startup")
async def startup_event():
    """Initialize databases, directories, and services on startup."""
    logger.info("="*60)
    logger.info("Starting Evaluaitor v%s", SERVICE_VERSION)
    logger.info("="*60)

    # Ensure required directories exist
    ensure_directories()

    # Initialize database
    logger.info("Initializing database...")
    db_status = init_database()

    if db_status["errors"]:
        for error in db_status["errors"]:
            logger.error("Database init error: %s", error)
    else:
        logger.info("Database initialized successfully")

    logger.info("Evaluaitor startup complete")


# ═══════════════════════════════════════════════════════════════
# Routers
# ═══════════════════════════════════════════════════════════════

from routers import system, organizations

app.include_router(system.router)
app.include_router(organizations.router)


# ═══════════════════════════════════════════════════════════════
# Static Files
# ═══════════════════════════════════════════════════════════════

# Create static dir if it doesn't exist (for file uploads)
os.makedirs(STATIC_PATH, exist_ok=True)
app.mount("/static", StaticFiles(directory=STATIC_PATH), name="static")


# ═══════════════════════════════════════════════════════════════
# CORS Middleware
# ═══════════════════════════════════════════════════════════════

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
