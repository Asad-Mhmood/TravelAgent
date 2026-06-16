"""
Custom Exception Hierarchy
==========================

Centralized exception handling with proper error codes,
user-friendly messages, and logging integration.

Design Pattern: Custom Exception Hierarchy
"""

from typing import Any, Dict, Optional
from fastapi import status


class TravelAgentException(Exception):
    """
    Base exception for all application errors.
    
    All custom exceptions should inherit from this class.
    """
    
    def __init__(
        self,
        message: str,
        error_code: str,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert exception to dictionary for API response"""
        return {
            "error": {
                "message": self.message,
                "code": self.error_code,
                "details": self.details
            }
        }


# ===== Client Errors (4xx) =====

class ValidationError(TravelAgentException):
    """Input validation failed"""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code="VALIDATION_ERROR",
            status_code=status.HTTP_400_BAD_REQUEST,
            details=details
        )


class AuthenticationError(TravelAgentException):
    """Authentication failed"""
    
    def __init__(self, message: str = "Authentication required"):
        super().__init__(
            message=message,
            error_code="AUTHENTICATION_ERROR",
            status_code=status.HTTP_401_UNAUTHORIZED
        )


class AuthorizationError(TravelAgentException):
    """Authorization failed"""
    
    def __init__(self, message: str = "Permission denied"):
        super().__init__(
            message=message,
            error_code="AUTHORIZATION_ERROR",
            status_code=status.HTTP_403_FORBIDDEN
        )


class NotFoundError(TravelAgentException):
    """Resource not found"""
    
    def __init__(self, resource: str, identifier: str):
        super().__init__(
            message=f"{resource} with ID '{identifier}' not found",
            error_code="NOT_FOUND",
            status_code=status.HTTP_404_NOT_FOUND,
            details={"resource": resource, "id": identifier}
        )


class RateLimitError(TravelAgentException):
    """Rate limit exceeded"""
    
    def __init__(self, retry_after: Optional[int] = None):
        super().__init__(
            message="Rate limit exceeded. Please try again later.",
            error_code="RATE_LIMIT_EXCEEDED",
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            details={"retry_after_seconds": retry_after} if retry_after else {}
        )


# ===== Service Errors (5xx) =====

class ServiceUnavailableError(TravelAgentException):
    """External service unavailable"""
    
    def __init__(self, service_name: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=f"{service_name} is currently unavailable",
            error_code="SERVICE_UNAVAILABLE",
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            details={"service": service_name, **(details or {})}
        )


class LiveKitConnectionError(TravelAgentException):
    """LiveKit connection failed"""
    
    def __init__(self, message: str = "Failed to connect to voice service"):
        super().__init__(
            message=message,
            error_code="LIVEKIT_CONNECTION_ERROR",
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE
        )


class MCPServerError(TravelAgentException):
    """MCP server error"""
    
    def __init__(self, server_name: str, message: str):
        super().__init__(
            message=f"{server_name} error: {message}",
            error_code="MCP_SERVER_ERROR",
            status_code=status.HTTP_502_BAD_GATEWAY,
            details={"server": server_name}
        )


class FlightSearchError(MCPServerError):
    """Flight search service error"""
    
    def __init__(self, message: str):
        super().__init__(server_name="Flight Search", message=message)


class AirbnbSearchError(MCPServerError):
    """Airbnb search service error"""
    
    def __init__(self, message: str):
        super().__init__(server_name="Airbnb Search", message=message)


# ===== Business Logic Errors =====

class InvalidSearchParametersError(ValidationError):
    """Invalid search parameters provided"""
    
    def __init__(self, parameter: str, reason: str):
        super().__init__(
            message=f"Invalid {parameter}: {reason}",
            details={"parameter": parameter, "reason": reason}
        )


class NoResultsFoundError(TravelAgentException):
    """Search returned no results"""
    
    def __init__(self, search_type: str):
        super().__init__(
            message=f"No {search_type} found matching your criteria",
            error_code="NO_RESULTS_FOUND",
            status_code=status.HTTP_404_NOT_FOUND,
            details={"search_type": search_type}
        )
