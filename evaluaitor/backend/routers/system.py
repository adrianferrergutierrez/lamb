"""
System router for Evaluaitor.

Provides health check and database status endpoints.
"""

import logging

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, inspect

from dependencies import verify_token
from database.connection import get_db, get_engine
from database.models import EvaluationJob, Organization, JobStatus
from schemas.system import HealthResponse, DatabaseStatusResponse, SQLiteStatus
from config import SERVICE_VERSION, SERVICE_NAME

logger = logging.getLogger("evaluaitor")

router = APIRouter(tags=["System"])


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health check",
    description="Check if the service is running. No authentication required.",
    responses={200: {"description": "Service is healthy"}},
)
async def health_check():
    """Health check endpoint — no authentication required."""
    return HealthResponse(
        status="ok",
        version=SERVICE_VERSION,
        service=SERVICE_NAME,
    )


@router.get(
    "/database/status",
    response_model=DatabaseStatusResponse,
    summary="Database status",
    description="Get database status and statistics. Requires authentication.",
    responses={
        200: {"description": "Database status"},
        401: {"description": "Unauthorized"},
    },
)
async def database_status(
    token: str = Depends(verify_token),
    db: Session = Depends(get_db),
):
    """Get database status and job/organization counts."""
    try:
        # Check if tables exist
        inspector = inspect(get_engine())
        tables = set(inspector.get_table_names())
        expected = {"organizations", "evaluation_jobs", "evaluation_results", "extracted_content"}
        schema_valid = expected.issubset(tables)

        # Get counts
        jobs_count = db.query(func.count(EvaluationJob.id)).scalar() or 0
        pending_jobs = db.query(func.count(EvaluationJob.id)).filter(
            EvaluationJob.status == JobStatus.PENDING
        ).scalar() or 0
        orgs_count = db.query(func.count(Organization.id)).scalar() or 0

        return DatabaseStatusResponse(
            sqlite_status=SQLiteStatus(initialized=True, schema_valid=schema_valid),
            jobs_count=jobs_count,
            pending_jobs=pending_jobs,
            organizations_count=orgs_count,
        )
    except Exception as e:
        logger.error("Database status check failed: %s", e)
        return DatabaseStatusResponse(
            sqlite_status=SQLiteStatus(initialized=False, schema_valid=False),
        )
