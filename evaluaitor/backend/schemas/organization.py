"""
Organization-related Pydantic schemas for Evaluaitor.
"""

from datetime import datetime
from typing import Optional, Dict, Any

from pydantic import BaseModel, Field


class OrganizationCreate(BaseModel):
    """Request body for creating/updating an organization."""
    external_id: str = Field(description="LAMB organization ID/slug")
    name: str = Field(description="Organization display name")
    config: Optional[Dict[str, Any]] = Field(default=None, description="Organization-specific settings")


class OrganizationResponse(BaseModel):
    """Organization response model."""
    id: int = Field(description="Internal organization ID")
    external_id: str = Field(description="LAMB organization ID/slug")
    name: str = Field(description="Organization display name")
    created_at: datetime = Field(description="Creation timestamp")
    updated_at: datetime = Field(description="Last update timestamp")

    model_config = {"from_attributes": True}


class OrganizationDetailResponse(OrganizationResponse):
    """Organization response with job statistics."""
    jobs_count: int = Field(default=0, description="Total evaluation jobs")
    pending_jobs: int = Field(default=0, description="Pending jobs")
    completed_jobs: int = Field(default=0, description="Completed jobs")
    failed_jobs: int = Field(default=0, description="Failed jobs")
