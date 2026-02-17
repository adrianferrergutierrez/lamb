"""
SQLAlchemy ORM models for Evaluaitor.

Defines the database schema for organizations, evaluation jobs, results,
and extracted content following the project specification.
"""

import enum
from datetime import datetime

from sqlalchemy import (
    Column, Integer, String, Text, Float, DateTime, ForeignKey,
    Enum, JSON, UniqueConstraint, Index
)
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


# ═══════════════════════════════════════════════════════════════
# Enums
# ═══════════════════════════════════════════════════════════════

class JobStatus(str, enum.Enum):
    """Evaluation job status."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


# ═══════════════════════════════════════════════════════════════
# Organizations (synced from LAMB)
# ═══════════════════════════════════════════════════════════════

class Organization(Base):
    """Organization model - synced from LAMB for multi-tenancy."""

    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    external_id = Column(String, nullable=False, unique=True, index=True)
    name = Column(String, nullable=False)
    config = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    jobs = relationship("EvaluationJob", back_populates="organization", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Organization(id={self.id}, external_id='{self.external_id}', name='{self.name}')>"


# ═══════════════════════════════════════════════════════════════
# Evaluation Jobs
# ═══════════════════════════════════════════════════════════════

class EvaluationJob(Base):
    """Evaluation job model - tracks evaluation requests and their processing status."""

    __tablename__ = "evaluation_jobs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    job_code = Column(String, nullable=False, unique=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False)

    # Evaluation Configuration
    evaluator_id = Column(String, nullable=False)  # LAMB assistant ID
    plugin_name = Column(String, nullable=False, default="rubric_eval")
    plugin_params = Column(JSON, default=dict)

    # Submission File
    original_filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    file_size = Column(Integer)
    content_type = Column(String)

    # Job Status
    status = Column(Enum(JobStatus), nullable=False, default=JobStatus.PENDING, index=True)

    # Progress Tracking
    progress_current = Column(Integer, default=0)
    progress_total = Column(Integer, default=0)
    progress_message = Column(String)

    # Timing
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    processing_started_at = Column(DateTime)
    processing_completed_at = Column(DateTime)

    # Error Handling
    error_message = Column(Text)
    error_details = Column(JSON)

    # Metadata
    client_reference = Column(String)  # Optional: LAMBA submission ID
    metadata_ = Column("metadata", JSON, default=dict)

    # Relationships
    organization = relationship("Organization", back_populates="jobs")
    result = relationship("EvaluationResult", back_populates="job", uselist=False, cascade="all, delete-orphan")
    extracted_content = relationship("ExtractedContent", back_populates="job", uselist=False, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<EvaluationJob(id={self.id}, job_code='{self.job_code}', status='{self.status}')>"


# ═══════════════════════════════════════════════════════════════
# Evaluation Results
# ═══════════════════════════════════════════════════════════════

class EvaluationResult(Base):
    """Evaluation result model - stores AI evaluation output."""

    __tablename__ = "evaluation_results"

    id = Column(Integer, primary_key=True, autoincrement=True)
    job_id = Column(Integer, ForeignKey("evaluation_jobs.id", ondelete="CASCADE"), nullable=False, unique=True)

    # Evaluation Output
    score = Column(Float)
    score_normalized = Column(Float)  # Normalized to 0-1 for LTI
    max_score = Column(Float, default=10.0)

    # Feedback
    feedback = Column(Text)
    feedback_structured = Column(JSON)  # Structured feedback (rubric criteria)

    # Raw Response
    raw_response = Column(Text)  # Full LLM response for debugging

    # Metadata
    model_used = Column(String)  # Which LAMB assistant/model
    tokens_used = Column(Integer)
    processing_time_ms = Column(Integer)

    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    job = relationship("EvaluationJob", back_populates="result")

    def __repr__(self):
        return f"<EvaluationResult(id={self.id}, job_id={self.job_id}, score={self.score})>"


# ═══════════════════════════════════════════════════════════════
# Extracted Content (cached)
# ═══════════════════════════════════════════════════════════════

class ExtractedContent(Base):
    """Extracted content model - caches text extracted from submitted documents."""

    __tablename__ = "extracted_content"

    id = Column(Integer, primary_key=True, autoincrement=True)
    job_id = Column(Integer, ForeignKey("evaluation_jobs.id", ondelete="CASCADE"), nullable=False)

    # Extracted Data
    content_text = Column(Text)
    content_preview = Column(Text)  # First N characters
    extraction_method = Column(String)  # pdf, docx, plain, etc.

    # Metadata
    page_count = Column(Integer)
    word_count = Column(Integer)
    char_count = Column(Integer)

    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    job = relationship("EvaluationJob", back_populates="extracted_content")

    def __repr__(self):
        return f"<ExtractedContent(id={self.id}, job_id={self.job_id}, method='{self.extraction_method}')>"
