"""
Enterprise Logging System
=========================

Structured logging with JSON output, correlation IDs, and
proper log levels for production monitoring.

Features:
- JSON structured logging
- Correlation ID tracking
- Performance metrics
- Error tracking
- Audit trails
"""

import logging
import sys
import json
from datetime import datetime
from typing import Any, Dict, Optional
from pathlib import Path
import traceback
from contextvars import ContextVar

from src.config import settings, Paths


# Context variable for request correlation
correlation_id: ContextVar[Optional[str]] = ContextVar('correlation_id', default=None)


class JSONFormatter(logging.Formatter):
    """
    Custom JSON formatter for structured logging.
    
    Outputs logs in JSON format for easy parsing by log aggregation tools
    like ELK Stack, Splunk, or CloudWatch.
    """
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON"""
        
        log_data: Dict[str, Any] = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # Add correlation ID if present
        corr_id = correlation_id.get()
        if corr_id:
            log_data["correlation_id"] = corr_id
        
        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = {
                "type": record.exc_info[0].__name__,
                "message": str(record.exc_info[1]),
                "traceback": traceback.format_exception(*record.exc_info)
            }
        
        # Add extra fields if present
        if hasattr(record, "extra_fields"):
            log_data.update(record.extra_fields)
        
        return json.dumps(log_data, default=str)


class TextFormatter(logging.Formatter):
    """Human-readable formatter for development"""
    
    def __init__(self):
        super().__init__(
            fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )


def setup_logging() -> None:
    """
    Configure application-wide logging.
    
    Sets up:
    - Console handler (stdout)
    - File handler (rotating)
    - JSON or text format based on environment
    - Appropriate log levels
    """
    
    # Root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper()))
    
    # Remove existing handlers
    root_logger.handlers.clear()
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    
    # File handler
    if settings.LOG_FILE:
        log_file = Paths.LOGS_DIR / settings.LOG_FILE
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
    else:
        file_handler = None
    
    # Choose formatter based on environment
    if settings.LOG_FORMAT == "json" and settings.ENVIRONMENT == "production":
        formatter = JSONFormatter()
    else:
        formatter = TextFormatter()
    
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    if file_handler:
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
    
    # Set third-party loggers to WARNING
    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("fastapi").setLevel(logging.WARNING)
    logging.getLogger("livekit").setLevel(logging.INFO)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance with the given name.
    
    Args:
        name: Logger name (usually __name__)
        
    Returns:
        Configured logger instance
    """
    return logging.getLogger(name)


class LoggerMixin:
    """
    Mixin class to add logging capability to any class.
    
    Usage:
        class MyClass(LoggerMixin):
            def my_method(self):
                self.logger.info("Doing something")
    """
    
    @property
    def logger(self) -> logging.Logger:
        """Get logger for this class"""
        return get_logger(self.__class__.__name__)


# Initialize logging on module import
setup_logging()
