"""Utility functions and helpers for the application."""

import logging
import sys
from datetime import datetime, timezone
from typing import Any


def setup_logging(level: int = logging.INFO) -> logging.Logger:
    """Configure structured logging for the application."""
    logger = logging.getLogger("python_notes_api")
    logger.setLevel(level)

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


def utc_now() -> datetime:
    """Return the current UTC datetime."""
    return datetime.now(timezone.utc)


def serialize_error(message: str, details: dict[str, Any] | None = None) -> dict[str, Any]:
    """Serialize a standardized error response."""
    response: dict[str, Any] = {"error": message}
    if details:
        response["details"] = details
    return response
