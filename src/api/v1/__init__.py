"""API v1 Routes"""
from fastapi import APIRouter

from .routes import sessions, search, health, chat

api_router = APIRouter()

# Register sub-routers
api_router.include_router(sessions.router, prefix="/sessions", tags=["Sessions"])
api_router.include_router(chat.router, prefix="/chat", tags=["Chat"])
api_router.include_router(search.router, prefix="/search", tags=["Search"])
api_router.include_router(health.router, prefix="/health", tags=["Health"])

__all__ = ["api_router"]
