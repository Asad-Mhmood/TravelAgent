# ✅ Setup Complete - Airbnb Travel Agent

Your LiveKit voice agent is now configured with Airbnb search capabilities!

## 🎯 What's Configured

### Voice Pipeline
- **Speech-to-Text**: Deepgram Nova-2 (high accuracy)
- **LLM**: Groq Llama 3.1 8B Instant (very fast, free tier)
- **Text-to-Speech**: Deepgram Aura Asteria (natural voice)
- **VAD**: Silero (voice activity detection)

### MCP Integration
- **Airbnb MCP Server**: Configured via `npx` (auto-downloads on first use)
- **Tools Available**:
  - `airbnb_search` - Search vacation rentals with filters
  - `airbnb_listing_details` - Get detailed property info

### Your Credentials (from .env)
```
✅ GROQ_API_KEY: Configured
✅ DEEPGRAM_API_KEY: Configured
✅ GOOGLE_API_KEY: Configured (optional backup)
✅ LIVEKIT_URL: ws://localhost:7880
✅ LIVEKIT_API_KEY: devkey
✅ LIVEKIT_API_SECRET: secret
✅ LLM_CHOICE: llama-3.1-8b-instant
```

## 🚀 Next Steps

### 1. Install Dependencies
```bash
uv sync
```

This will install:
- livekit-agents with MCP support
- livekit-plugins-groq (for LLM)
- livekit-plugins-deepgram (for STT and TTS)
- livekit-plugins-silero (for VAD)
- All other required packages

### 2. Download Models
```bash
uv run python livekit_mcp_agent.py download-files
```

### 3. Start LiveKit Server (if not running)
If you have a local LiveKit server at `ws://localhost:7880`, make sure it's running.

### 4. Run the Agent

**Option A: Console Mode (recommended for testing)**
```bash
uv run python livekit_mcp_agent.py console
```

**Option B: Connect to LiveKit Server**
```bash
uv run python livekit_mcp_agent.py dev
```

**Option C: Production Mode**
```bash
uv run python livekit_mcp_agent.py start
```

## 🎤 Test Conversation Examples

Once the agent is running, try:

1. **"Find me a place to stay in San Francisco"**
2. **"Search for a 2-bedroom apartment in Paris for 2 adults"**
3. **"Show me pet-friendly homes in Miami under $200 per night"**
4. **"Find entire homes in Tokyo from June 15 to June 20"**

## 🔧 Configuration Files

- **livekit_mcp_agent.py** - Main agent with Groq + Airbnb integration
- **.env** - Your API keys and configuration
- **pyproject.toml** - Python dependencies
- **QUICKSTART.md** - Quick reference guide
- **AIRBNB_SETUP.md** - Detailed Airbnb integration docs

## 💡 Why This Stack?

### Groq (LLM)
- ⚡ **Extremely fast** inference (much faster than OpenAI)
- 💰 **Free tier** available with generous limits
- 🎯 **High quality** responses with Llama 3.1

### Deepgram (STT & TTS)
- 🎙️ **Best-in-class** speech recognition
- 🔊 **Natural voice** synthesis
- 💰 **Free tier** for development
- ⚡ **Low latency** streaming

### Airbnb MCP Server
- 🏠 **No API key required** for Airbnb
- 🌍 **International support** with proper geocoding
- 🔍 **Advanced filters** (dates, guests, price, property type)
- 📦 **Easy setup** via `npx`

## 📊 Cost Breakdown (Approximate)

| Service | Free Tier | Cost After Free |
|---------|-----------|-----------------|
| Groq | 30 requests/min | Very affordable |
| Deepgram STT | 200 hours/month | $0.0043/min |
| Deepgram TTS | Free tier | $0.015/1K chars |
| Airbnb MCP | Free (no API key) | Free |
| LiveKit (self-hosted) | Free | Free |

**For development**: Likely stays within free tiers!

## 🛠️ Customization Options

### Change LLM Model
Edit `.env`:
```bash
# Faster but smaller
LLM_CHOICE=llama-3.1-8b-instant

# Slower but smarter
LLM_CHOICE=llama-3.1-70b-versatile

# Best for coding tasks
LLM_CHOICE=mixtral-8x7b-32768
```

### Change TTS Voice
Edit `livekit_mcp_agent.py`:
```python
tts=deepgram.TTS(
    voice="aura-asteria-en",  # Female, neutral
    # Other options:
    # "aura-luna-en"      # Female, expressive
    # "aura-stella-en"    # Female, warm
    # "aura-athena-en"    # Female, professional
    # "aura-hera-en"      # Female, clear
    # "aura-orion-en"     # Male, deep
    # "aura-arcas-en"     # Male, friendly
    # "aura-perseus-en"   # Male, confident
    # "aura-angus-en"     # Male, Scottish
    # "aura-orpheus-en"   # Male, smooth
    # "aura-helios-en"    # Male, energetic
    # "aura-zeus-en"      # Male, authoritative
    model="aura-asteria-en",
),
```

### Add More MCP Servers
Edit `livekit_mcp_agent.py`:
```python
mcp_servers=[
    # Airbnb
    mcp.MCPServerStdio(
        name="airbnb",
        command="npx",
        args=["-y", "@openbnb/mcp-server-airbnb", "--ignore-robots-txt"],
    ),
    # Add weather, flights, etc.
    # mcp.MCPServerStdio(
    #     name="weather",
    #     command="npx",
    #     args=["-y", "@some/weather-mcp-server"],
    # ),
],
```

## 🐛 Troubleshooting

### Node.js not found
```bash
# Windows
winget install OpenJS.NodeJS.LTS

# Verify
node --version
npx --version
```

### Groq API Error
- Check your API key at https://console.groq.com/keys
- Verify no spaces in `.env` file
- Check rate limits (30 req/min on free tier)

### Deepgram API Error
- Verify API key at https://console.deepgram.com
- Check free tier limits haven't been exceeded

### Airbnb MCP Not Working
- Ensure Node.js 18+ is installed
- First run downloads the package (takes 10-30 seconds)
- Check `--ignore-robots-txt` flag is present
- Try running manually: `npx -y @openbnb/mcp-server-airbnb --ignore-robots-txt`

### LiveKit Connection Issues
- Ensure LiveKit server is running at `ws://localhost:7880`
- Check firewall isn't blocking the connection
- Try console mode first: `uv run python livekit_mcp_agent.py console`

## 📚 Documentation

- **Quick Start**: See `QUICKSTART.md`
- **Full README**: See `README.md`
- **Airbnb Details**: See `AIRBNB_SETUP.md`
- **LiveKit Docs**: https://docs.livekit.io/agents/
- **Groq Docs**: https://console.groq.com/docs
- **Deepgram Docs**: https://developers.deepgram.com/

## 🎉 You're Ready!

Your travel agent is configured and ready to help users find their perfect vacation rental through natural voice conversations!

Run the agent with:
```bash
uv sync
uv run python livekit_mcp_agent.py download-files
uv run python livekit_mcp_agent.py console
```

Then say: **"Find me an apartment in Paris for next weekend!"** 🗼🏠
