"""
Chat Service - AI Conversation Management
==========================================

Integrates Groq LLM with MCP servers for intelligent travel assistance.
"""

import uuid
from typing import Dict, Any, Optional
from groq import Groq

from src.config import settings
from src.core import get_logger, LoggerMixin

logger = get_logger(__name__)


class ChatService(LoggerMixin):
    """
    Manages AI chat conversations with tool calling.
    
    Integrates:
    - Groq LLM for natural language understanding
    - Flight Search MCP server
    - Airbnb Search MCP server
    """
    
    def __init__(self):
        """Initialize chat service with Groq client"""
        self.groq_client = Groq(api_key=settings.GROQ_API_KEY)
        self.model = settings.LLM_CHOICE
        
        # Conversation context (in-memory, move to Redis for production)
        self.conversations = {}
        
        self.logger.info("ChatService initialized")
    
    async def process_message(
        self, 
        message: str, 
        session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Process user message and generate AI response.
        
        Args:
            message: User's message
            session_id: Optional session ID for context
            
        Returns:
            Dict containing response, session_id, and metadata
        """
        # Generate session ID if not provided
        if not session_id:
            session_id = str(uuid.uuid4())
        
        # Get or create conversation history
        if session_id not in self.conversations:
            self.conversations[session_id] = self._initialize_conversation()
        
        conversation = self.conversations[session_id]
        
        # Add user message to history
        conversation.append({
            "role": "user",
            "content": message
        })
        
        self.logger.info(f"Processing message in session {session_id}")
        
        try:
            # Call Groq API with optimized parameters
            response = self.groq_client.chat.completions.create(
                model=self.model,
                messages=conversation,
                temperature=0.3,  # Lower for more focused responses
                max_tokens=1500,
                top_p=0.9,
            )
            
            # Extract assistant response
            assistant_message = response.choices[0].message.content
            
            # Add to conversation history
            conversation.append({
                "role": "assistant",
                "content": assistant_message
            })
            
            # Keep conversation size manageable (last 10 messages)
            if len(conversation) > 11:  # system + 10 messages
                conversation = [conversation[0]] + conversation[-10:]
                self.conversations[session_id] = conversation
            
            return {
                "response": assistant_message,
                "session_id": session_id,
                "tool_calls": None,  # TODO: Add MCP tool calling
                "metadata": {
                    "model": self.model,
                    "tokens_used": response.usage.total_tokens if hasattr(response, 'usage') else None
                }
            }
            
        except Exception as e:
            self.logger.exception(f"Error processing message: {e}")
            raise
    
    def _initialize_conversation(self) -> list:
        """
        Initialize conversation with system prompt.
        
        Returns:
            List with system message
        """
        return [{
            "role": "system",
            "content": """You are an intelligent AI travel assistant. Your job is to extract travel information and provide helpful responses.

CRITICAL RULES:
1. EXTRACT information from user messages - don't keep asking for what they already told you
2. When user says "Dubai to Sri Lanka" or "Dubai to Colombo" - YOU HAVE the departure and destination
3. When user says "21 June" or "21st June" - YOU HAVE the date
4. When user says "one passenger" or "I'm traveling" - assume 1 passenger unless stated otherwise
5. DEFAULT to one-way ticket unless user mentions return

RESPONSE FORMAT:
- If you have ALL info (origin, destination, date, passengers): Say "Let me search for flights..." and list what you understood
- If you're MISSING critical info, ask ONLY for what's missing
- NEVER ask for information the user already provided

EXAMPLES OF GOOD RESPONSES:

User: "Dubai to Colombo, June 21, one passenger"
You: "Perfect! Let me search for one-way flights from Dubai (DXB) to Colombo (CMB) on June 21st for 1 passenger. 

Based on typical routes, here are approximate options:
- Emirates: ~$300-400 (direct, 4 hours)
- FlyDubai: ~$250-350 (direct)
- Sri Lankan Airlines: ~$280-380 (direct)

Note: These are estimated prices. Actual prices vary based on availability and booking time. Would you like me to help you find accommodations in Colombo as well?"

User: "Flight from Dubai to Sri Lanka"
You: "Great! I can help you find flights from Dubai to Sri Lanka. I just need a couple more details:
- Which city in Sri Lanka? (Colombo is the main airport - CMB)
- Travel date?
- Number of passengers?"

User: "21 June"
You: "Got it - June 21st. And which city would you like to fly from, and to where?"

INFORMATION EXTRACTION:
- Dubai, DXB, Dubai Airport = Dubai International Airport
- Sri Lanka, Colombo, CMB = Bandaranaike International Airport (Colombo)
- "21 June", "June 21", "21st June" = June 21st of current year
- "one passenger", "just me", "1 person" = 1 passenger
- If not mentioned, assume: 1 adult passenger, one-way ticket

BE EFFICIENT. Don't waste the user's time asking for info they already gave you."""
        }]
