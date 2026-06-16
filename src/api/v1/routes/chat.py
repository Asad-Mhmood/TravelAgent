"""
Chat API - AI Conversation Endpoint
====================================

Handles chat messages and integrates with Groq LLM + MCP servers
"""

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional, List
import asyncio

from src.core import get_logger
from src.services.chat_service import ChatService

logger = get_logger(__name__)
router = APIRouter()


# ===== Request/Response Models =====

class ChatMessage(BaseModel):
    """Chat message from user"""
    message: str = Field(..., min_length=1, max_length=2000, description="User message")
    session_id: Optional[str] = Field(None, description="Session ID for conversation context")


class ChatResponse(BaseModel):
    """AI response"""
    response: str = Field(..., description="AI assistant response")
    session_id: str = Field(..., description="Session ID")
    tool_calls: Optional[List[dict]] = Field(default=None, description="Tools that were called")
    metadata: Optional[dict] = Field(default_factory=dict, description="Additional metadata")


# ===== Endpoints =====

@router.post("/message", response_model=ChatResponse)
async def send_message(chat_message: ChatMessage):
    """
    Send a message to the AI travel assistant.
    
    The AI can:
    - Search for flights using the Flight MCP server
    - Search for Airbnb accommodations using the Airbnb MCP server
    - Provide travel recommendations and planning assistance
    
    Args:
        chat_message: User message and optional session ID
        
    Returns:
        AI response with any tool results
        
    Raises:
        HTTPException: If processing fails
    """
    try:
        logger.info(
            "Processing chat message",
            extra={"extra_fields": {"message_preview": chat_message.message[:100]}}
        )
        
        # Initialize chat service
        chat_service = ChatService()
        
        # Process message with AI
        response = await chat_service.process_message(
            message=chat_message.message,
            session_id=chat_message.session_id
        )
        
        logger.info(
            "Chat response generated",
            extra={"extra_fields": {"session_id": response["session_id"]}}
        )
        
        return ChatResponse(**response)
        
    except Exception as e:
        logger.exception("Failed to process chat message", exc_info=e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process message: {str(e)}"
        )


@router.get("/history/{session_id}")
async def get_chat_history(session_id: str):
    """
    Get conversation history for a session.
    
    Args:
        session_id: Session identifier
        
    Returns:
        List of messages in the conversation
    """
    # TODO: Implement conversation history storage/retrieval
    return {"session_id": session_id, "messages": []}
