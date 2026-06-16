# 🔌 Connect Frontend to Real AI

## ✅ What I Just Created:

1. **Backend Chat API** (`src/api/v1/routes/chat.py`)
   - POST `/api/v1/chat/message` - Send messages to AI

2. **Chat Service** (`src/services/chat_service.py`)
   - Uses your **Groq API** with Llama 3.1
   - Maintains conversation context
   - Proper system prompt for travel assistant

3. **Frontend API Client** (`frontend/src/services/api.js`)
   - Ready to connect to backend

## 🚀 Setup Steps:

### Step 1: Install Groq Package
```bash
# Stop the backend (Ctrl+C)
uv sync
```

### Step 2: Restart Backend
```bash
$env:PYTHONPATH="c:\Asad Mehmood\TravelAgent"
uv run uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

### Step 3: Update Frontend VoiceAgentPage

Replace the `handleSendMessage` function in `frontend/src/pages/VoiceAgentPage.jsx`:

**Find this (around line 73):**
```javascript
// Simulate AI response (replace with actual API call)
setTimeout(() => {
  const responses = [
    "I'd be happy to help you find flights! Could you tell me your departure city and destination?",
    ...
  ];
```

**Replace with:**
```javascript
// REAL API CALL
try {
  const result = await fetch('http://localhost:8000/api/v1/chat/message', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      message: userMessage,
      session_id: sessionId.current
    })
  });
  
  const data = await result.json();
  addMessage('assistant', data.response);
  speakText(data.response);
} catch (error) {
  console.error('API Error:', error);
  addMessage('assistant', 'Sorry, I had trouble processing that. Please try again.');
  toast.error('Failed to get response');
}
setIsProcessing(false);
```

### Step 4: Add Session ID

At the top of VoiceAgentPage component (around line 12), add:
```javascript
const sessionId = useRef(null);

// Initialize session ID
useEffect(() => {
  sessionId.current = `session-${Date.now()}`;
}, []);
```

## 🎯 Complete Updated Code:

I'll create the updated file for you...
