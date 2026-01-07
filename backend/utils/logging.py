"""
Logging utilities for structured logging with request tracking.
"""
import logging
import sys
import time
from contextvars import ContextVar
from typing import Optional
import uuid

# Context variable for request ID tracking
request_id_var: ContextVar[Optional[str]] = ContextVar("request_id", default=None)


class RequestIdFilter(logging.Filter):
    """Add request ID to log records."""

    def filter(self, record):
        record.request_id = request_id_var.get() or "N/A"
        return True


def setup_logging(log_level: str = "INFO"):
    """Configure structured logging for the application."""
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - [%(request_id)s] - %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )

    # Add request ID filter to root logger
    for handler in logging.root.handlers:
        handler.addFilter(RequestIdFilter())


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance with the given name."""
    return logging.getLogger(name)


def set_request_id(req_id: Optional[str] = None):
    """Set request ID for current context."""
    if req_id is None:
        req_id = str(uuid.uuid4())
    request_id_var.set(req_id)
    return req_id


def get_request_id() -> Optional[str]:
    """Get current request ID."""
    return request_id_var.get()


class Timer:
    """Simple timer for measuring operation duration."""

    def __init__(self):
        self.start_time = None
        self.end_time = None

    def __enter__(self):
        self.start_time = time.time()
        return self

    def __exit__(self, *args):
        self.end_time = time.time()

    @property
    def elapsed(self) -> float:
        """Get elapsed time in seconds."""
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return 0.0
