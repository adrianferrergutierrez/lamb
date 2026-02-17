"""
Evaluaitor configuration management.

Centralizes all environment variable access with sensible defaults.
"""

import os
import logging
from pathlib import Path

logger = logging.getLogger("evaluaitor")


# ═══════════════════════════════════════════════════════════════
# Authentication
# ═══════════════════════════════════════════════════════════════
API_KEY = os.getenv("EVALUAITOR_API_KEY", "0p3n-w3bu!")

# ═══════════════════════════════════════════════════════════════
# LAMB Integration
# ═══════════════════════════════════════════════════════════════
LAMB_API_URL = os.getenv("LAMB_API_URL", "http://localhost:9099")
LAMB_TIMEOUT = int(os.getenv("LAMB_TIMEOUT", "120"))

# ═══════════════════════════════════════════════════════════════
# Database
# ═══════════════════════════════════════════════════════════════
DATABASE_PATH = os.getenv("DATABASE_PATH", "data/evaluaitor.db")

# ═══════════════════════════════════════════════════════════════
# File Storage
# ═══════════════════════════════════════════════════════════════
STATIC_PATH = os.getenv("STATIC_PATH", "static")
MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", "100"))
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024

# ═══════════════════════════════════════════════════════════════
# Processing
# ═══════════════════════════════════════════════════════════════
DEFAULT_TIMEOUT_SECONDS = int(os.getenv("DEFAULT_TIMEOUT_SECONDS", "120"))
MAX_CONCURRENT_JOBS = int(os.getenv("MAX_CONCURRENT_JOBS", "10"))

# ═══════════════════════════════════════════════════════════════
# Service Info
# ═══════════════════════════════════════════════════════════════
SERVICE_NAME = "evaluaitor"
SERVICE_VERSION = "0.1.0"


def ensure_directories():
    """Ensure required directories exist."""
    dirs = [
        Path(DATABASE_PATH).parent,
        Path(STATIC_PATH),
    ]
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)
        logger.info("Ensured directory exists: %s", d)
