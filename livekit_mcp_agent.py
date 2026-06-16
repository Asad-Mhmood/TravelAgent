"""
LiveKit Voice Agent
==================
Main agent implementation file. This is a starter template - replace with your actual agent code.
"""

from dotenv import load_dotenv
from livekit import rtc
from livekit import agents
from livekit.agents import (
    NOT_GIVEN,
    Agent,
    AgentFalseInterruptionEvent,
    AgentSession,
    JobContext,
    JobProcess,
    MetricsCollectedEvent,
    ModelSettings,
    RoomInputOptions,
    RoomOutputOptions,
    RunContext,
    WorkerOptions,
    cli,
    metrics,
    mcp
)
# Simplified turn detection - no heavy ML models needed
# from livekit.plugins.turn_detector.multilingual import MultilingualModel
from livekit.agents.llm import function_tool
from livekit.plugins import openai, deepgram, silero, groq
from datetime import datetime
import logging
import os

# uncomment to enable Krisp background voice/noise cancellation
# from livekit.plugins import noise_cancellation

# Load environment variables
load_dotenv(".env")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def prewarm(proc: JobProcess):
    proc.userdata["vad"] = silero.VAD.load()


class Assistant(Agent):
    """Main voice assistant implementation."""
    
    def __init__(self):
        super().__init__(
            instructions="""You are a helpful and friendly travel assistant voice AI.
            
            You help users with complete travel planning including:
            - Searching Airbnb vacation rentals
            - Finding and comparing flight options
            - Providing detailed property and flight information
            
            You speak clearly and naturally, as if having a phone conversation with a travel agent.
            Be concise but warm in your responses.
            
            AIRBNB SEARCHES:
            - Ask for: location, dates, and number of guests
            - Use the airbnb_search tool to find available properties
            - Present results conversationally with price, type, and key features
            - Use airbnb_listing_details for more information
            - Always set ignoreRobotsText to true for Airbnb tools
            
            FLIGHT SEARCHES:
            - Ask for: origin, destination, dates, and number of passengers
            - Use flight search tools to find available flights
            - Compare prices across different dates if helpful
            - Provide booking URLs when available
            - Mention airline, price, duration, and stops
            
            COMBINED TRAVEL PLANNING:
            - You can search for both accommodations AND flights
            - Help users plan complete trips
            - Compare total trip costs
            - Suggest optimal travel dates based on prices
            
            If you don't know something, be honest about it."""
        )       
    
    async def on_enter(self):
        """Called when the agent becomes active."""
        logger.info("Agent session started")
        
        # Generate initial greeting
        await self.session.generate_reply(
            instructions="Greet the user warmly and ask how you can help them today."
        )
    
    async def on_exit(self):
        """Called when the agent session ends."""
        logger.info("Agent session ended")


async def entrypoint(ctx: agents.JobContext):
    """Main entry point for the agent worker."""
    
    logger.info(f"Agent started in room: {ctx.room.name}")
    
    # Configure the voice pipeline
    session = AgentSession(
        # Speech-to-Text
        stt=deepgram.STT(
            model="nova-2",
            language="en",
        ),
        
        # Large Language Model (using Groq for fast inference)
        llm=groq.LLM(
            model=os.getenv("LLM_CHOICE", "llama-3.1-8b-instant"),
            temperature=0.7,
        ),
        
        # Text-to-Speech (using Deepgram)
        tts=deepgram.TTS(
            model="aura-asteria-en",
        ),
        
        # Voice Activity Detection
        vad=silero.VAD.load(),
        
        # Turn detection strategy - using simple server-side VAD (no ML models needed)
        # turn_detection=MultilingualModel(),  # Disabled - requires PyTorch

        # ==========================================
        # MCP SERVERS CONFIGURATION
        # ==========================================
        # Add or remove MCP servers here to extend agent capabilities
        
        mcp_servers=[
            # ------------------------------------------
            # AIRBNB - Vacation Rental Search
            # ------------------------------------------
            # Purpose: Search for vacation rentals and get property details
            # Tools: airbnb_search, airbnb_listing_details
            # No API key required
            mcp.MCPServerStdio(
                command="npx",
                args=["-y", "@openbnb/mcp-server-airbnb", "--ignore-robots-txt"],
            ),
            
            # ------------------------------------------
            # FLIGHT SEARCH - Real-time Flight Data
            # ------------------------------------------
            # Purpose: Search flights, compare prices, get booking URLs
            # Tools: Flight search with flexible dates
            # API: https://flights.fctolabs.com/
            mcp.MCPServerHTTP(
                url="https://flights.fctolabs.com/mcp",
            ),
            
            # ------------------------------------------
            # ADD MORE MCP SERVERS BELOW
            # ------------------------------------------
            # Template for stdio-based servers (like Airbnb):
            # mcp.MCPServerStdio(
            #     command="npx",
            #     args=["-y", "package-name"],
            # ),
            #
            # Template for HTTP-based servers (like Flight Search):
            # mcp.MCPServerHTTP(
            #     url="https://api.example.com/mcp",
            # ),
        ],
    )
    
    # Start the session
    await session.start(
        room=ctx.room,
        agent=Assistant(),
        # room_input_options=RoomInputOptions(
            # Enable noise cancellation
            # noise_cancellation=noise_cancellation.BVC(),
            # For telephony, use: noise_cancellation.BVCTelephony()
        # ),
        room_output_options=RoomOutputOptions(transcription_enabled=True),
    )
    
    # Handle session events
    @session.on("agent_state_changed")
    def on_state_changed(ev):
        """Log agent state changes."""
        logger.info(f"State: {ev.old_state} -> {ev.new_state}")
    
    @session.on("user_started_speaking")
    def on_user_speaking():
        """Track when user starts speaking."""
        logger.debug("User started speaking")
    
    @session.on("user_stopped_speaking")
    def on_user_stopped():
        """Track when user stops speaking."""
        logger.debug("User stopped speaking")


if __name__ == "__main__":
    # Run the agent using LiveKit CLI
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint, prewarm_fnc=prewarm))