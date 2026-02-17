"""
System-related Pydantic schemas for Evaluaitor.
"""

from pydantic import BaseModel, Field
from typing import Optional


class HealthResponse(BaseModel):
    """Health check response."""
    status: str = Field(default="ok", description="Service status")
    version: str = Field(description="Service version")
    service: str = Field(default="evaluaitor", description="Service name")


class SQLiteStatus(BaseModel):
    """SQLite database status."""
    initialized: bool = Field(description="Whether the database is initialized")
    schema_valid: bool = Field(default=True, description="Whether the schema is valid")


class DatabaseStatusResponse(BaseModel):
    """Database status response."""
    sqlite_status: SQLiteStatus = Field(description="SQLite status")
    jobs_count: int = Field(default=0, description="Total evaluation jobs")
    pending_jobs: int = Field(default=0, description="Pending evaluation jobs")
    organizations_count: int = Field(default=0, description="Registered organizations")
