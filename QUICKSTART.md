# Quick Start Guide - Airbnb Voice Agent

Get your Airbnb-powered voice agent running in 5 minutes!

## Step 1: Install Node.js

The Airbnb MCP server requires Node.js 18 or later.

**Check if you have Node.js:**
```bash
node --version
```

**If not installed, download from:**
- Windows: https://nodejs.org/ (download the LTS installer)
- Or use: `winget install OpenJS.NodeJS.LTS`

## Step 2: Install Python Dependencies

```bash
# Install all dependencies using UV
uv sync
```

## Step 3: Set Up Environment Variables

1. Copy the example environment file:
```bash
copy .env.example .env
```

2. Edit `.env` and add your API keys:
```
GROQ_API_KEY=gsk-your-key-here
DEEPGRAM_API_KEY=your-deepgram-key-here
LIVEKIT_URL=ws://localhost:7880
LIVEKIT_API_KEY=devkey
LIVEKIT_API_SECRET=secret
```

**Get API Keys:**
- Groq: https://console.groq.com/keys (free tier available!)
- Deepgram: https://console.deepgram.com (free tier available)

## Step 4: Download Required Models

```bash
# Download VAD and turn detection models
uv run python livekit_mcp_agent.py download-files
```

## Step 5: Test Your Agent

```bash
# Run in console mode (no LiveKit server needed)
uv run python livekit_mcp_agent.py console
```

## Step 6: Try It Out!

Once the agent starts, try saying:

- **"Find me a place to stay in San Francisco"**
- **"Search for a 2-bedroom apartment in Paris for next weekend"**
- **"Show me pet-friendly homes in Miami under $200 per night"**

The agent will use the Airbnb MCP server to search and respond with property listings!

## What's Happening Behind the Scenes?

```
Your Voice ──▶ Deepgram (STT) ──▶ Groq Llama 3.1 (LLM) ──▶ Airbnb MCP ──▶ Response
                                        │
                                        ▼
                                  Deepgram (TTS) ──▶ Your Speakers
```

## Troubleshooting

### "Command 'npx' not found"
- Install Node.js (see Step 1)
- Restart your terminal after installation

### "OpenAI API key not found"
- Not needed! We're using Groq instead (faster and free tier)

### "Groq API key not found"
- Check your `.env` file has `GROQ_API_KEY=gsk-...`
- Get a free key from https://console.groq.com/keys
- Make sure there are no spaces around the `=`

### "Deepgram API key not found"
- Check your `.env` file has `DEEPGRAM_API_KEY=...`
- Get a free key from https://console.deepgram.com

### First search is slow
- Normal! The Airbnb MCP server downloads on first use (~10-30 seconds)
- Subsequent searches will be much faster

### No search results
- The agent should automatically set `ignoreRobotsText=true`
- Try a broader location (e.g., "Paris" instead of a street address)

## Next Steps

1. **Deploy to LiveKit Cloud** - See README.md for full deployment guide
2. **Add more MCP servers** - Extend with weather, flights, etc.
3. **Customize the agent** - Edit instructions in `livekit_mcp_agent.py`
4. **Add custom tools** - Create your own `@function_tool` methods

## Need Help?

- **Full Documentation**: See [README.md](README.md)
- **Airbnb Integration Details**: See [AIRBNB_SETUP.md](AIRBNB_SETUP.md)
- **LiveKit Docs**: https://docs.livekit.io/agents/

---

Happy building! 🎤🏠✨
