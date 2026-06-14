# LiveKit Voice Agent

A LiveKit-powered voice AI agent framework that demonstrates how to build realtime conversational AI with MCP (Model Context Protocol) server integration.

## Features

- 🎤 Natural voice conversations with low latency
- 🔄 Real-time voice interaction with interruption handling
- 🏠 **Airbnb vacation rental search** with advanced filtering (location, dates, guests, price)
- 🛠️ Tool integration via MCP servers
- 🎯 Multiple provider options (OpenAI, Deepgram, Cartesia, etc.)
- 🔌 Extensible architecture for custom tools and agents

## Prerequisites

- Python 3.9 or later
- Node.js 18+ (required for Airbnb MCP server)
- API Keys:
  - Groq API key (for LLM - fast and free tier available)
  - Deepgram API key (for STT and TTS)
  - LiveKit server (local or cloud)

## Quick Start

### 1. Install Dependencies

```bash
# Install dependencies using UV
uv sync
```

### 2. Set Up Environment Variables

Copy `.env.example` to `.env` and fill in your credentials:

```bash
cp .env.example .env
```

**Required variables:**
- `GROQ_API_KEY` - Groq API key (free tier available)
- `DEEPGRAM_API_KEY` - Deepgram API key (for STT and TTS)
- `LIVEKIT_URL` - LiveKit server URL (e.g., `ws://localhost:7880` for local)
- `LIVEKIT_API_KEY` - LiveKit API key (use `devkey` for local)
- `LIVEKIT_API_SECRET` - LiveKit API secret (use `secret` for local)

### 3. Download Required Model Files

Before first run, download the required model files (Silero VAD, turn detector):

```bash
# Download model files for basic agent
uv run python livekit_basic_agent.py download-files

# Download model files for MCP agent
uv run python livekit_mcp_agent.py download-files
```

### 4. Run the Agent

```bash
# Basic agent (minimal configuration)
uv run python livekit_basic_agent.py console

# MCP agent (with MCP server integration)
uv run python livekit_mcp_agent.py console

# Development mode (connects to LiveKit - optional)
uv run python livekit_basic_agent.py dev

# Production mode
uv run python livekit_basic_agent.py start
```

## Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   LiveKit   │────▶│ Voice Agent  │────▶│   Airbnb    │
│   Client    │     │   (Python)   │     │ MCP Server  │
└─────────────┘     └──────────────┘     └─────────────┘
                           │
                    ┌──────┴──────┐
                    │             │
              ┌─────▼────┐  ┌────▼─────┐
              │ Deepgram │  │   Groq   │
              │ STT+TTS  │  │   LLM    │
              └──────────┘  └──────────┘

Voice Pipeline:
User Voice → Deepgram STT → Groq Llama 3.1 → Airbnb Search → Deepgram TTS → Audio Output
```

## Project Files

### Basic Agent

**`livekit_basic_agent.py`** - The simplest possible LiveKit voice agent
- Minimal configuration with only essential components
- Great for learning and testing basic functionality
- Requires only OpenAI and Deepgram API keys
- Includes example tool: `get_current_date_and_time`

### MCP Agent

**`livekit_mcp_agent.py`** - Full-featured voice agent with:
- Configurable speech-to-text, LLM, and text-to-speech providers
- MCP server integration for tool calling
- Multilingual turn detection
- Event handling and state management
- Logging and metrics support

## Voice Pipeline Configuration

The agent uses a modular voice pipeline with swappable components:

### Speech-to-Text (STT)
- **Default**: Deepgram Nova-2 (highest accuracy)
- Alternatives: AssemblyAI, Azure Speech, Whisper

### Large Language Model (LLM)
- **Default**: Groq Llama 3.1 8B Instant (very fast, free tier available)
- Alternatives: Groq Llama 3.1 70B, OpenAI GPT-4, Anthropic Claude, Google Gemini

### Text-to-Speech (TTS)
- **Default**: Deepgram Aura (natural, fast)
- Alternatives: OpenAI, Cartesia, ElevenLabs

### Voice Activity Detection (VAD)
- **Default**: Silero VAD (reliable voice detection)

### Turn Detection
- **Default**: Multilingual Model (natural conversation flow)
- Alternatives: Semantic model, VAD-based

## MCP Server Integration

The agent supports integration with MCP (Model Context Protocol) servers for extending functionality with custom tools.

### Airbnb Integration

The voice agent comes pre-configured with the [Airbnb MCP server](https://github.com/openbnb-org/mcp-server-airbnb) which enables:

- **Search Airbnb listings** with advanced filters (location, dates, guests, price range, property type)
- **Get detailed property information** including amenities, house rules, and booking links
- **International location support** with accurate geocoding
- **No API key required** - works out of the box

**Available Tools:**
1. `airbnb_search` - Search for vacation rentals with filters
2. `airbnb_listing_details` - Get detailed information about a specific property

**Example Voice Interactions:**
- "Find me a 2-bedroom apartment in Paris for next weekend"
- "Search for pet-friendly homes in San Francisco under $200 per night"
- "Show me details about listing 12345678"

**Prerequisites:**
- Node.js 18+ must be installed for `npx` to work
- The MCP server will be automatically downloaded on first use

### Configuring MCP Servers

In `livekit_mcp_agent.py`:

```python
session = AgentSession(
    # ... other config ...
    mcp_servers=[
        # Airbnb MCP server (stdio-based)
        mcp.MCPServerStdio(
            name="airbnb",
            command="npx",
            args=["-y", "@openbnb/mcp-server-airbnb", "--ignore-robots-txt"],
        ),
        # Add more MCP servers here
    ]
)
```

**Other MCP Server Types:**

```python
# HTTP-based MCP server
mcp.MCPServerHTTP(url="http://localhost:8089/mcp")

# Stdio-based MCP server (like Airbnb)
mcp.MCPServerStdio(
    name="server-name",
    command="npx",
    args=["-y", "package-name"]
)
```

### Adding Custom Tools

You can also add tools directly to your agent using the `@function_tool` decorator:

```python
from livekit.agents import function_tool, RunContext
from datetime import datetime

class Assistant(Agent):
    @function_tool
    async def get_current_time(self, context: RunContext) -> str:
        """Get the current time."""
        return datetime.now().strftime("%I:%M %p")
```

## Development

### Project Structure

```
livekit-agent/
├── livekit_basic_agent.py   # Basic example agent
├── livekit_mcp_agent.py     # MCP-enabled agent
├── pyproject.toml           # Dependencies
├── .env.example             # Environment template
├── Dockerfile               # Container deployment
└── README.md
```

### Installing Additional Providers

```bash
# Additional TTS providers
uv add livekit-plugins-cartesia livekit-plugins-elevenlabs

# Additional LLM providers
uv add livekit-plugins-anthropic livekit-plugins-google livekit-plugins-groq

# Additional STT providers
uv add livekit-plugins-assemblyai livekit-plugins-azure
```

## Deploy to LiveKit Cloud

Once you've tested your agent locally, deploy it to LiveKit Cloud for production use:

### 1. Create a LiveKit Cloud Account

Sign up at [LiveKit Cloud](https://cloud.livekit.io/)

### 2. Install the LiveKit CLI

Choose the installation method for your platform:

**Windows:**
```bash
winget install LiveKit.LiveKitCLI
```

**Mac:**
```bash
brew install livekit
```

**Linux:**
```bash
curl -sSL https://get.livekit.io/ | bash
```

### 3. Authenticate with LiveKit Cloud

Open a new terminal and authenticate:

```bash
lk cloud auth
```

### 4. Configure Environment Variables

Set up your environment variables for the cloud:

```bash
lk app env -w
```

This will write your LiveKit credentials to `.env.local`

### 5. Start Your Agent

Run your agent connected to LiveKit Cloud:

```bash
uv run python livekit_basic_agent.py start
```

### 6. Create an Agent in LiveKit Cloud

In a separate terminal, register your agent:

```bash
lk agent create
```

### 7. Test in the Playground

Visit the [LiveKit Agents Playground](https://agents-playground.livekit.io/) and sign in with your LiveKit organization to test your agent in the browser.

### 8. Telephony Integration (Optional)

To integrate your agent with phone calling systems, see the [LiveKit Telephony documentation](https://docs.livekit.io/agents/start/telephony/)

## Performance Optimization

### Reduce Latency
- Use regional deployments close to users
- Choose faster providers (Deepgram for STT, Cartesia for TTS)
- Use streaming where possible

### Scale Efficiently
- Set appropriate prewarm counts in `livekit.toml` for production
- Use connection pooling for external API calls
- Implement caching for frequently accessed data

## Console Mode Testing

Console mode lets you test your agent locally without needing a LiveKit server:

```bash
# Test the basic agent
uv run python livekit_basic_agent.py console

# Test the MCP agent
uv run python livekit_mcp_agent.py console
```

This will start an interactive console where you can speak to your agent using your microphone and speakers.

## Troubleshooting

### Python Version
Ensure you're using Python 3.9 or later:
```bash
python --version
```

### Model Downloads
TTS models may download on first use, which can take time. The Docker image pre-downloads Silero VAD to speed up startup.

### API Key Issues
- Verify all required API keys are set in `.env`
- Check that API keys are valid and have sufficient credits
- Ensure no extra whitespace in environment variable values

### Audio Issues in Console Mode
- Check microphone/speaker permissions
- Verify audio devices are correctly configured
- Try adjusting VAD sensitivity if voice detection is problematic

## Environment Variables Reference

| Variable | Required | Description |
|----------|----------|-------------|
| `GROQ_API_KEY` | Yes | Groq API key for LLM (free tier available) |
| `DEEPGRAM_API_KEY` | Yes | Deepgram API key for STT and TTS |
| `LIVEKIT_URL` | Yes | LiveKit server URL (`ws://localhost:7880` for local) |
| `LIVEKIT_API_KEY` | Yes | LiveKit API key (`devkey` for local dev) |
| `LIVEKIT_API_SECRET` | Yes | LiveKit API secret (`secret` for local dev) |
| `LLM_CHOICE` | No | Model selection (default: llama-3.1-8b-instant) |
| `GOOGLE_API_KEY` | No | Google Gemini API key (alternative LLM) |
| `LOG_LEVEL` | No | Logging level (default: INFO) |

## Resources

- [LiveKit Agents Documentation](https://docs.livekit.io/agents/)
- [LiveKit Python SDK](https://github.com/livekit/agents)
