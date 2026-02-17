"""
Evaluation-related Pydantic schemas for Evaluaitor.

These schemas define the request/response models for the evaluation endpoints.
Stubs for Phase 2 implementation.
"""

from datetime import datetime
from typing import Optional, Dict, Any, List
from enum import Enum

from pydantic import BaseModel, Field


class JobStatusEnum(str, Enum):
    """Evaluation job status (mirrors database enum)."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class EvaluationSubmitResponse(BaseModel):
    """Response after submitting an evaluation job."""
    job_code: str = Field(description="Unique job identifier")
    status: JobStatusEnum = Field(default=JobStatusEnum.PENDING, description="Initial job status")
    message: str = Field(default="Evaluation job queued successfully", description="Status message")
    created_at: datetime = Field(description="Job creation timestamp")


class ProgressInfo(BaseModel):
    """Job progress information."""
    current: int = Field(default=0, description="Current progress step")
    total: int = Field(default=0, description="Total progress steps")
    percentage: float = Field(default=0.0, description="Progress percentage")
    message: Optional[str] = Field(default=None, description="Progress message")


class EvaluationStatusResponse(BaseModel):
    """Evaluation job status response."""
    job_code: str = Field(description="Unique job identifier")
    status: JobStatusEnum = Field(description="Current job status")
    progress: ProgressInfo = Field(description="Progress information")
    created_at: datetime = Field(description="Job creation timestamp")
    processing_started_at: Optional[datetime] = Field(default=None, description="Processing start time")
    processing_completed_at: Optional[datetime] = Field(default=None, description="Processing completion time")
    processing_duration_seconds: Optional[float] = Field(default=None, description="Processing duration")
    error_message: Optional[str] = Field(default=None, description="Error message if failed")


class EvaluationResultData(BaseModel):
    """Evaluation result data."""
    score: Optional[float] = Field(default=None, description="Numeric score")
    score_normalized: Optional[float] = Field(default=None, description="Normalized score (0-1)")
    max_score: float = Field(default=10.0, description="Maximum possible score")
    feedback: Optional[str] = Field(default=None, description="AI-generated feedback")
    feedback_structured: Optional[Dict[str, Any]] = Field(default=None, description="Structured feedback")
    model_used: Optional[str] = Field(default=None, description="Model/assistant used")
    processing_time_ms: Optional[int] = Field(default=None, description="Processing time in ms")


class EvaluationResultResponse(BaseModel):
    """Evaluation result response."""
    job_code: str = Field(description="Unique job identifier")
    status: JobStatusEnum = Field(description="Job status")
    result: Optional[EvaluationResultData] = Field(default=None, description="Evaluation result")
    client_reference: Optional[str] = Field(default=None, description="Client-provided reference")
    message: Optional[str] = Field(default=None, description="Status message")


class EvaluationJobSummary(BaseModel):
    """Summary of an evaluation job for list responses."""
    job_code: str = Field(description="Unique job identifier")
    evaluator_id: str = Field(description="LAMB assistant ID used")
    plugin_name: str = Field(description="Evaluation plugin used")
    status: JobStatusEnum = Field(description="Job status")
    original_filename: str = Field(description="Submitted filename")
    created_at: datetime = Field(description="Job creation timestamp")
    processing_completed_at: Optional[datetime] = Field(default=None, description="Completion time")
    client_reference: Optional[str] = Field(default=None, description="Client reference")

    model_config = {"from_attributes": True}


class EvaluationListResponse(BaseModel):
    """Response for listing evaluation jobs."""
    total: int = Field(description="Total number of jobs matching filters")
    items: List[EvaluationJobSummary] = Field(description="List of evaluation jobs")
