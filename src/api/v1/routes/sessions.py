"""
Voice Session Management API
============================

Handles LiveKit voice session creation and management.
"""

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import uuid

from src.core import get_logger
from src.services.livekit_service import LiveKitService

logger = get_logger(__name__)
router = APIRouter()


# ===== Request/Response Models =====

class CreateSessionRequest(BaseModel):
    """Request to create a new voice session"""
    user_id: Optional[str] = Field(None, description="Optional user identifier")
    metadata: Optional[dict] = Field(default_factory=dict, description="Additional metadata")


class SessionResponse(BaseModel):
    """Voice session details"""
    session_id: str = Field(..., description="Unique session identifier")
    token: str = Field(..., description="LiveKit access token")
    url: str = Field(..., description="LiveKit server URL")
    created_at: datetime = Field(..., description="Session creation timestamp")
    expires_at: datetime = Field(..., description="Token expiration")


# ===== Endpoints =====

@router.post("/", response_model=SessionResponse, status_code=status.HTTP_201_CREATED)
async def create_voice_session(request: CreateSessionRequest):
    """
    Create a new voice interaction session.
    
    This endpoint generates a LiveKit token for the client to connect
    to the voice agent.
    
    Args:
        request: Session creation parameters
        
    Returns:
        Session details including LiveKit token
        
    Raises:
        HTTPException: If session creation fails
    """
    try:
        session_id = str(uuid.uuid4())
        
        logger.info(
            "Creating voice session",
            extra={"extra_fields": {"session_id": session_id, "user_id": request.user_id}}
        )
        
        # Create LiveKit session
        livekit_service = LiveKitService()
        session_data = await livekit_service.create_session(
            session_id=session_id,
            user_id=request.user_id or "guest",
            metadata=request.metadata
        )
        
        logger.info(
            "Voice session created successfully",
            extra={"extra_fields": {"session_id": session_id}}
        )
        
        return SessionResponse(**session_data)
        
    except Exception as e:
        logger.exception("Failed to create voice session", exc_info=e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create voice session"
        )


@router.get("/{session_id}", response_model=SessionResponse)
async def get_session(session_id: str):
    """
    Get details of an existing session.
    
    Args:
        session_id: Session identifier
        
    Returns:
        Session details
        
    Raises:
        HTTPException: If session not found
    """
    # TODO: Implement session retrieval from database/cache
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Session retrieval not yet implemented"
    )


@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
async def end_session(session_id: str):
    """
    End an active voice session.
    
    Args:
        session_id: Session identifier
        
    Raises:
        HTTPException: If session not found or cannot be ended
    """
    logger.info("Ending voice session", extra={"extra_fields": {"session_id": session_id}})
    
    # TODO: Implement session cleanup
    return None
