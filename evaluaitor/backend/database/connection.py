"""
Database connection management for Evaluaitor.

Handles SQLite initialization, engine creation, and session management.
"""

import logging
from pathlib import Path

from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker

from config import DATABASE_PATH

logger = logging.getLogger("evaluaitor")

# Module-level engine and session factory
_engine = None
_SessionLocal = None


def get_engine():
    """Get or create the SQLAlchemy engine (singleton).

    Returns:
        SQLAlchemy Engine instance
    """
    global _engine
    if _engine is None:
        # Ensure data directory exists
        db_path = Path(DATABASE_PATH)
        db_path.parent.mkdir(parents=True, exist_ok=True)

        db_url = f"sqlite:///{db_path}"
        _engine = create_engine(
            db_url,
            connect_args={"check_same_thread": False},  # Required for SQLite + FastAPI
            echo=False,
        )
        logger.info("Database engine created: %s", db_url)
    return _engine


def get_session_factory():
    """Get or create the session factory (singleton).

    Returns:
        SQLAlchemy SessionLocal class
    """
    global _SessionLocal
    if _SessionLocal is None:
        _SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=get_engine(),
        )
    return _SessionLocal


def init_database() -> dict:
    """Initialize the database: create tables if they don't exist.

    Returns:
        Dictionary with initialization status and any errors
    """
    errors = []
    try:
        from database.models import Base

        engine = get_engine()

        # Create all tables
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created/verified successfully")

        # Verify tables exist
        inspector = inspect(engine)
        expected_tables = {"organizations", "evaluation_jobs", "evaluation_results", "extracted_content"}
        actual_tables = set(inspector.get_table_names())
        missing = expected_tables - actual_tables

        if missing:
            msg = f"Missing tables after creation: {missing}"
            logger.error(msg)
            errors.append(msg)
        else:
            logger.info("All expected tables present: %s", expected_tables)

    except Exception as e:
        msg = f"Failed to initialize database: {e}"
        logger.error(msg)
        errors.append(msg)

    return {
        "initialized": len(errors) == 0,
        "errors": errors,
    }


def get_db():
    """FastAPI dependency that yields a database session.

    Usage:
        @app.get("/example")
        async def example(db: Session = Depends(get_db)):
            ...

    Yields:
        SQLAlchemy Session
    """
    SessionLocal = get_session_factory()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
