# 🚀 START HERE - Airbnb Travel Voice Agent

## 👋 Welcome!

Your Airbnb-powered voice travel agent is ready! This guide gets you running in 3 minutes.

## 📋 Prerequisites Check

Before starting, verify you have:
- ✅ **Python 3.9+**: Run `python --version`
- ✅ **Node.js 18+**: Run `node --version`
- ✅ **UV**: Run `uv --version`

Missing something? See [CHECKLIST.md](CHECKLIST.md) for installation links.

## 🏃 Quick Start (3 steps)

### 1️⃣ Install Dependencies (30 seconds)
```bash
uv sync
```

### 2️⃣ Download Models (30 seconds)
```bash
uv run python livekit_mcp_agent.py download-files
```

### 3️⃣ Run the Agent (immediately!)
```bash
uv run python livekit_mcp_agent.py console
```

## 🎤 First Conversation

Wait for the agent to greet you, then say:

> **"Find me a place to stay in San Francisco"**

The agent will:
1. 🎙️ **Hear** your voice (Deepgram STT)
2. 🧠 **Understand** your request (Groq Llama 3.1)
3. 🔍 **Search** Airbnb properties (Airbnb MCP)
4. 🔊 **Respond** naturally (Deepgram TTS)

## 📚 Documentation

**Choose your path:**

### 🏃 I want to start quickly
→ Read [QUICKSTART.md](QUICKSTART.md) (5 minutes)

### 🔧 I want to understand the setup
→ Read [SETUP_COMPLETE.md](SETUP_COMPLETE.md) (10 minutes)

### 🏠 I want Airbnb integration details
→ Read [AIRBNB_SETUP.md](AIRBNB_SETUP.md) (15 minutes)

### 📖 I want full documentation
→ Read [README.md](README.md) (20 minutes)

### 📊 I want the big picture
→ Read [SUMMARY.md](SUMMARY.md) (10 minutes)

### ✅ I want a checklist
→ Read [CHECKLIST.md](CHECKLIST.md) (ongoing)

## 🎯 What's Configured

```
Your Voice → Deepgram STT → Groq Llama 3.1 → Airbnb MCP → Deepgram TTS → Audio
             (recognize)    (understand)       (search)     (speak)
```

### API Keys Used (from .env)
- ✅ **Groq**: Fast LLM (free tier)
- ✅ **Deepgram**: STT + TTS (free tier)
- ✅ **Airbnb MCP**: No API key needed!
- ✅ **LiveKit**: Local server (free)

### Features Available
- 🔍 Search Airbnb by location, dates, guests, price
- 🏠 Get detailed property information
- 🌍 International location support
- 🎙️ Natural voice conversations
- ⚡ Fast responses (< 2 seconds)

## 🧪 Test Commands

Try these phrases with the agent:

```
"Find me a place in Paris"
"Search for a 2-bedroom apartment in Tokyo for next week"
"Show me pet-friendly homes in Miami under $200"
"Find entire homes in London from March 15 to March 20"
```

## 🐛 Troubleshooting

### Agent won't start
```bash
# Check Python
python --version  # Should be 3.9+

# Check Node.js
node --version    # Should be 18+

# Reinstall dependencies
uv sync
```

### No voice input/output
- Check microphone permissions
- Verify speakers/headphones connected
- Try adjusting volume

### Airbnb search fails
- First search is slow (downloads MCP server)
- Check Node.js is installed
- Verify internet connection

### API key errors
```bash
# Check .env file exists
type .env

# Verify keys have no spaces
# Good: GROQ_API_KEY=gsk_abc123
# Bad:  GROQ_API_KEY = gsk_abc123
```

## 💡 Next Steps

After your first successful conversation:

1. **Explore**: Try different search queries
2. **Customize**: Edit agent instructions in `livekit_mcp_agent.py`
3. **Extend**: Add more MCP servers for weather, flights, etc.
4. **Deploy**: Move to production with LiveKit Cloud

## 🆘 Need Help?

### Quick Answers
→ Check [CHECKLIST.md](CHECKLIST.md) troubleshooting section

### Detailed Help
→ See [AIRBNB_SETUP.md](AIRBNB_SETUP.md) troubleshooting

### Community Support
- LiveKit Discord: https://livekit.io/discord
- Groq Discord: https://groq.com/discord
- Airbnb MCP Issues: https://github.com/openbnb-org/mcp-server-airbnb/issues

## 🎁 Bonus Features

Your setup includes:

- **Free tier friendly**: Most usage stays free during development
- **Fast inference**: Groq is 10x faster than OpenAI GPT-4
- **Natural voice**: Deepgram Aura TTS sounds great
- **No API key for Airbnb**: Works out of the box
- **Production ready**: Can deploy to LiveKit Cloud

## 📊 Expected Performance

| Metric | Target |
|--------|--------|
| STT Latency | ~80ms |
| LLM Response | ~300ms |
| TTS Latency | ~150ms |
| **Total** | **~1.5s** |

## 🏆 Success Checklist

You're successful when:
- ✅ Agent greets you on start
- ✅ Your voice is recognized
- ✅ Agent responds naturally
- ✅ Airbnb search returns results
- ✅ Audio output is clear

## 🚀 Ready? Let's Go!

```bash
# One command to rule them all:
uv sync && uv run python livekit_mcp_agent.py download-files && uv run python livekit_mcp_agent.py console
```

Then say: **"Find me an apartment in Paris!"** 🗼

---

**Built with:**
- 🎙️ [LiveKit Agents](https://docs.livekit.io/agents/)
- ⚡ [Groq](https://groq.com/) (LLM)
- 🔊 [Deepgram](https://deepgram.com/) (STT/TTS)
- 🏠 [Airbnb MCP Server](https://github.com/openbnb-org/mcp-server-airbnb)

**Happy building!** 🎉
