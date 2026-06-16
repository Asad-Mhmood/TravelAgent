"""
FastAPI Application Entry Point
================================

Professional FastAPI application with:
- Proper middleware stack
- Error handling
- CORS configuration
- Health checks
- API versioning
- OpenAPI documentation

Architecture: Clean Architecture / Layered Architecture
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import uuid
import time

from src.config import settings, Paths
from src.core import get_logger, correlation_id, TravelAgentException
from src.api.v1 import api_router

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    
    Handles startup and shutdown events.
    """
    # Startup
    logger.info(
        "Starting TravelAgent API",
        extra={
            "extra_fields": {
                "version": settings.APP_VERSION,
                "environment": settings.ENVIRONMENT
            }
        }
    )
    
    yield
    
    # Shutdown
    logger.info("Shutting down TravelAgent API")


# ===== Application Instance =====

app = FastAPI(
    title=settings.APP_NAME,
    description="Professional AI-Powered Travel Planning Platform",
    version=settings.APP_VERSION,
    docs_url="/api/docs" if settings.DEBUG else None,
    redoc_url="/api/redoc" if settings.DEBUG else None,
    openapi_url="/api/openapi.json" if settings.DEBUG else None,
    lifespan=lifespan
)


# ===== Middleware Stack =====

@app.middleware("http")
async def correlation_id_middleware(request: Request, call_next):
    """
    Add correlation ID to all requests for tracking.
    
    Correlation IDs help track requests across services and logs.
    """
    corr_id = request.headers.get("X-Correlation-ID") or str(uuid.uuid4())
    correlation_id.set(corr_id)
    
    response = await call_next(request)
    response.headers["X-Correlation-ID"] = corr_id
    
    return response


@app.middleware("http")
async def request_timing_middleware(request: Request, call_next):
    """
    Log request timing for performance monitoring.
    """
    start_time = time.time()
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    
    logger.info(
        f"{request.method} {request.url.path}",
        extra={
            "extra_fields": {
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "process_time": process_time
            }
        }
    )
    
    return response


# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# GZip compression for responses
app.add_middleware(GZipMiddleware, minimum_size=1000)


# ===== Exception Handlers =====

@app.exception_handler(TravelAgentException)
async def travel_agent_exception_handler(request: Request, exc: TravelAgentException):
    """Handle custom application exceptions"""
    logger.error(
        f"Application error: {exc.message}",
        extra={
            "extra_fields": {
                "error_code": exc.error_code,
                "details": exc.details
            }
        }
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.to_dict()
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle unexpected exceptions"""
    logger.exception("Unhandled exception occurred", exc_info=exc)
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "message": "An unexpected error occurred",
                "code": "INTERNAL_SERVER_ERROR",
                "details": {} if not settings.DEBUG else {"exception": str(exc)}
            }
        }
    )


# ===== Route Registration =====

# API v1 routes
app.include_router(api_router, prefix="/api/v1")

# Static files (for serving React build)
if Paths.STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(Paths.STATIC_DIR)), name="static")


# ===== Health Check Endpoints =====

@app.get("/health", tags=["System"])
async def health_check():
    """
    Basic health check endpoint.
    
    Returns:
        Service status and version
    """
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT
    }


@app.get("/health/ready", tags=["System"])
async def readiness_check():
    """
    Readiness check - verify all dependencies are available.
    
    Returns:
        Detailed readiness status
    """
    # TODO: Add checks for LiveKit, MCP servers, etc.
    checks = {
        "api": "ready",
        "livekit": "ready",  # TODO: Implement actual check
        "mcp_servers": "ready",  # TODO: Implement actual check
    }
    
    all_ready = all(status == "ready" for status in checks.values())
    
    return {
        "ready": all_ready,
        "checks": checks
    }


@app.get("/", tags=["System"])
async def root():
    """Root endpoint - API information"""
    return {
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "docs": "/api/docs" if settings.DEBUG else "disabled",
        "health": "/health"
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "src.api.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG,
        workers=1 if settings.DEBUG else settings.API_WORKERS,
        log_level=settings.LOG_LEVEL.lower()
    )
