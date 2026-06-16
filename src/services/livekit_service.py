"""LiveKit service - placeholder"""
from datetime import datetime, timedelta

class LiveKitService:
    async def create_session(self, session_id: str, user_id: str, metadata: dict):
        # Simplified for now
        return {
            "session_id": session_id,
            "token": "demo-token",
            "url": "ws://localhost:7880",
            "created_at": datetime.now(),
            "expires_at": datetime.now() + timedelta(hours=1)
        }
