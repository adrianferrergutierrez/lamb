"""
Database service layer for Evaluaitor.

Provides CRUD operations for organizations, evaluation jobs, and results.
"""

import uuid
import logging
from datetime import datetime
from typing import Optional, Dict, Any, List

from sqlalchemy.orm import Session
from sqlalchemy import func

from database.models import (
    Organization,
    EvaluationJob,
    EvaluationResult,
    ExtractedContent,
    JobStatus,
)

logger = logging.getLogger("evaluaitor")


# ═══════════════════════════════════════════════════════════════
# Organization Operations
# ═══════════════════════════════════════════════════════════════

class OrganizationService:
    """CRUD operations for organizations."""

    @staticmethod
    def create_or_update(db: Session, external_id: str, name: str, config: dict = None) -> Organization:
        """Create a new organization or update an existing one (upsert).

        Args:
            db: Database session
            external_id: LAMB organization ID
            name: Organization name
            config: Optional organization config

        Returns:
            Created or updated Organization
        """
        org = db.query(Organization).filter(Organization.external_id == external_id).first()

        if org:
            org.name = name
            if config is not None:
                org.config = config
            org.updated_at = datetime.utcnow()
            logger.info("Updated organization: %s", external_id)
        else:
            org = Organization(
                external_id=external_id,
                name=name,
                config=config or {},
            )
            db.add(org)
            logger.info("Created organization: %s", external_id)

        db.commit()
        db.refresh(org)
        return org

    @staticmethod
    def get_by_external_id(db: Session, external_id: str) -> Optional[Organization]:
        """Get an organization by its external ID.

        Args:
            db: Database session
            external_id: LAMB organization ID

        Returns:
            Organization or None
        """
        return db.query(Organization).filter(Organization.external_id == external_id).first()

    @staticmethod
    def get_job_stats(db: Session, organization_id: int) -> Dict[str, int]:
        """Get job statistics for an organization.

        Args:
            db: Database session
            organization_id: Internal organization ID

        Returns:
            Dictionary with jobs_count, pending_jobs, completed_jobs, failed_jobs
        """
        total = db.query(func.count(EvaluationJob.id)).filter(
            EvaluationJob.organization_id == organization_id
        ).scalar() or 0

        pending = db.query(func.count(EvaluationJob.id)).filter(
            EvaluationJob.organization_id == organization_id,
            EvaluationJob.status == JobStatus.PENDING,
        ).scalar() or 0

        completed = db.query(func.count(EvaluationJob.id)).filter(
            EvaluationJob.organization_id == organization_id,
            EvaluationJob.status == JobStatus.COMPLETED,
        ).scalar() or 0

        failed = db.query(func.count(EvaluationJob.id)).filter(
            EvaluationJob.organization_id == organization_id,
            EvaluationJob.status == JobStatus.FAILED,
        ).scalar() or 0

        return {
            "jobs_count": total,
            "pending_jobs": pending,
            "completed_jobs": completed,
            "failed_jobs": failed,
        }


# ═══════════════════════════════════════════════════════════════
# Evaluation Job Operations
# ═══════════════════════════════════════════════════════════════

class JobService:
    """CRUD operations for evaluation jobs."""

    @staticmethod
    def create_job(
        db: Session,
        organization_id: int,
        evaluator_id: str,
        original_filename: str,
        file_path: str,
        file_size: int = None,
        content_type: str = None,
        plugin_name: str = "rubric_eval",
        plugin_params: dict = None,
        client_reference: str = None,
        metadata: dict = None,
    ) -> EvaluationJob:
        """Create a new evaluation job.

        Args:
            db: Database session
            organization_id: Organization ID
            evaluator_id: LAMB assistant ID
            original_filename: Original submitted filename
            file_path: Path to stored file
            file_size: File size in bytes
            content_type: MIME type
            plugin_name: Evaluation plugin to use
            plugin_params: Plugin-specific parameters
            client_reference: Optional client reference (e.g., LAMBA submission ID)
            metadata: Optional additional metadata

        Returns:
            Created EvaluationJob
        """
        job_code = f"ev_{uuid.uuid4().hex[:16]}"

        job = EvaluationJob(
            job_code=job_code,
            organization_id=organization_id,
            evaluator_id=evaluator_id,
            plugin_name=plugin_name,
            plugin_params=plugin_params or {},
            original_filename=original_filename,
            file_path=file_path,
            file_size=file_size,
            content_type=content_type,
            status=JobStatus.PENDING,
            client_reference=client_reference,
            metadata_=metadata or {},
        )
        db.add(job)
        db.commit()
        db.refresh(job)

        logger.info("Created evaluation job: %s", job_code)
        return job

    @staticmethod
    def get_by_code(db: Session, job_code: str) -> Optional[EvaluationJob]:
        """Get a job by its job code.

        Args:
            db: Database session
            job_code: Unique job code

        Returns:
            EvaluationJob or None
        """
        return db.query(EvaluationJob).filter(EvaluationJob.job_code == job_code).first()

    @staticmethod
    def update_status(
        db: Session,
        job: EvaluationJob,
        status: JobStatus,
        progress_current: int = None,
        progress_total: int = None,
        progress_message: str = None,
        error_message: str = None,
        error_details: dict = None,
    ) -> EvaluationJob:
        """Update job status and progress.

        Args:
            db: Database session
            job: EvaluationJob to update
            status: New status
            progress_current: Current progress step
            progress_total: Total progress steps
            progress_message: Progress description
            error_message: Error message (if failed)
            error_details: Error details (if failed)

        Returns:
            Updated EvaluationJob
        """
        job.status = status

        if progress_current is not None:
            job.progress_current = progress_current
        if progress_total is not None:
            job.progress_total = progress_total
        if progress_message is not None:
            job.progress_message = progress_message

        if status == JobStatus.PROCESSING and job.processing_started_at is None:
            job.processing_started_at = datetime.utcnow()
        elif status in (JobStatus.COMPLETED, JobStatus.FAILED, JobStatus.CANCELLED):
            job.processing_completed_at = datetime.utcnow()

        if error_message:
            job.error_message = error_message
        if error_details:
            job.error_details = error_details

        db.commit()
        db.refresh(job)
        return job

    @staticmethod
    def list_jobs(
        db: Session,
        organization_id: int,
        status: Optional[JobStatus] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> List[EvaluationJob]:
        """List evaluation jobs with optional filtering.

        Args:
            db: Database session
            organization_id: Organization ID
            status: Optional status filter
            limit: Max results
            offset: Pagination offset

        Returns:
            List of EvaluationJob
        """
        query = db.query(EvaluationJob).filter(
            EvaluationJob.organization_id == organization_id
        )

        if status:
            query = query.filter(EvaluationJob.status == status)

        return query.order_by(EvaluationJob.created_at.desc()).offset(offset).limit(limit).all()

    @staticmethod
    def count_jobs(db: Session, organization_id: int, status: Optional[JobStatus] = None) -> int:
        """Count jobs for an organization.

        Args:
            db: Database session
            organization_id: Organization ID
            status: Optional status filter

        Returns:
            Job count
        """
        query = db.query(func.count(EvaluationJob.id)).filter(
            EvaluationJob.organization_id == organization_id
        )
        if status:
            query = query.filter(EvaluationJob.status == status)
        return query.scalar() or 0


# ═══════════════════════════════════════════════════════════════
# Evaluation Result Operations
# ═══════════════════════════════════════════════════════════════

class ResultService:
    """CRUD operations for evaluation results."""

    @staticmethod
    def create_result(
        db: Session,
        job_id: int,
        score: float = None,
        score_normalized: float = None,
        max_score: float = 10.0,
        feedback: str = None,
        feedback_structured: dict = None,
        raw_response: str = None,
        model_used: str = None,
        tokens_used: int = None,
        processing_time_ms: int = None,
    ) -> EvaluationResult:
        """Create an evaluation result.

        Args:
            db: Database session
            job_id: Associated job ID
            score: Numeric score
            score_normalized: Normalized score (0-1)
            max_score: Maximum possible score
            feedback: AI-generated feedback text
            feedback_structured: Structured feedback JSON
            raw_response: Full LLM response
            model_used: Model/assistant used
            tokens_used: Token consumption
            processing_time_ms: Processing time in ms

        Returns:
            Created EvaluationResult
        """
        result = EvaluationResult(
            job_id=job_id,
            score=score,
            score_normalized=score_normalized,
            max_score=max_score,
            feedback=feedback,
            feedback_structured=feedback_structured,
            raw_response=raw_response,
            model_used=model_used,
            tokens_used=tokens_used,
            processing_time_ms=processing_time_ms,
        )
        db.add(result)
        db.commit()
        db.refresh(result)

        logger.info("Created evaluation result for job_id=%d, score=%s", job_id, score)
        return result

    @staticmethod
    def get_by_job_id(db: Session, job_id: int) -> Optional[EvaluationResult]:
        """Get result by job ID.

        Args:
            db: Database session
            job_id: Job ID

        Returns:
            EvaluationResult or None
        """
        return db.query(EvaluationResult).filter(EvaluationResult.job_id == job_id).first()
