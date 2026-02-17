"""
Organizations router for Evaluaitor.

Provides endpoints for registering and querying organizations (synced from LAMB).
"""

import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from dependencies import verify_token
from database.connection import get_db
from database.service import OrganizationService
from schemas.organization import (
    OrganizationCreate,
    OrganizationResponse,
    OrganizationDetailResponse,
)

logger = logging.getLogger("evaluaitor")

router = APIRouter(prefix="/organizations", tags=["Organizations"])


@router.post(
    "",
    response_model=OrganizationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register or update an organization",
    description="Create a new organization or update an existing one (upsert by external_id).",
    responses={
        201: {"description": "Organization created/updated successfully"},
        401: {"description": "Unauthorized"},
    },
)
async def create_or_update_organization(
    org_data: OrganizationCreate,
    token: str = Depends(verify_token),
    db: Session = Depends(get_db),
):
    """Register or update an organization."""
    org = OrganizationService.create_or_update(
        db=db,
        external_id=org_data.external_id,
        name=org_data.name,
        config=org_data.config,
    )
    return org


@router.get(
    "/{external_id}",
    response_model=OrganizationDetailResponse,
    summary="Get organization details",
    description="Get an organization by its external ID, including job statistics.",
    responses={
        200: {"description": "Organization details"},
        401: {"description": "Unauthorized"},
        404: {"description": "Organization not found"},
    },
)
async def get_organization(
    external_id: str,
    token: str = Depends(verify_token),
    db: Session = Depends(get_db),
):
    """Get an organization by external ID with job stats."""
    org = OrganizationService.get_by_external_id(db, external_id)
    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Organization not found: {external_id}",
        )

    # Get job stats
    stats = OrganizationService.get_job_stats(db, org.id)

    return OrganizationDetailResponse(
        id=org.id,
        external_id=org.external_id,
        name=org.name,
        created_at=org.created_at,
        updated_at=org.updated_at,
        **stats,
    )
