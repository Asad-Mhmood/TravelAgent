"""Core package - logging, exceptions, and utilities"""
from .logger import get_logger, LoggerMixin, correlation_id
from .exceptions import (
    TravelAgentException,
    ValidationError,
    AuthenticationError,
    NotFoundError,
    RateLimitError,
    ServiceUnavailableError,
    LiveKitConnectionError,
    MCPServerError,
    FlightSearchError,
    AirbnbSearchError,
)

__all__ = [
    "get_logger",
    "LoggerMixin",
    "correlation_id",
    "TravelAgentException",
    "ValidationError",
    "AuthenticationError",
    "NotFoundError",
    "RateLimitError",
    "ServiceUnavailableError",
    "LiveKitConnectionError",
    "MCPServerError",
    "FlightSearchError",
    "AirbnbSearchError",
]
