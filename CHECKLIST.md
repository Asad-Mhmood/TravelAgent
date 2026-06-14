# ✅ Setup Checklist

## Prerequisites
- [ ] Python 3.9+ installed (`python --version`)
- [ ] Node.js 18+ installed (`node --version`)
- [ ] UV package manager installed (`uv --version`)
- [ ] LiveKit server running at ws://localhost:7880 (or accessible)

## API Keys
- [x] Groq API key obtained from https://console.groq.com/keys
- [x] Deepgram API key obtained from https://console.deepgram.com
- [x] Google API key (optional, for backup LLM)
- [x] .env file created with all keys

## Installation
- [ ] Run `uv sync` to install Python dependencies
- [ ] Run `uv run python livekit_mcp_agent.py download-files` to get models
- [ ] Verify no errors during installation

## Configuration
- [x] .env file configured with correct API keys
- [x] LIVEKIT_URL set to ws://localhost:7880
- [x] LIVEKIT_API_KEY and LIVEKIT_API_SECRET set
- [x] LLM_CHOICE set to llama-3.1-8b-instant
- [x] Agent instructions updated for travel assistance
- [x] Airbnb MCP server configured in livekit_mcp_agent.py

## Testing
- [ ] Run `uv run python livekit_mcp_agent.py console`
- [ ] Agent starts without errors
- [ ] Agent greets you when started
- [ ] Try: "Find me a place in San Francisco"
- [ ] Airbnb search returns results
- [ ] Voice input/output working correctly

## Verification
- [ ] Speech-to-text (STT) recognizes your voice
- [ ] LLM generates appropriate responses
- [ ] Airbnb MCP server searches successfully
- [ ] Text-to-speech (TTS) sounds natural
- [ ] Response latency is acceptable (< 2-3 seconds)

## Common Issues

### ❌ "Command 'npx' not found"
**Solution**: Install Node.js 18+ and restart terminal

### ❌ "Groq API key not found"
**Solution**: Check .env file has `GROQ_API_KEY=gsk-...` with no spaces

### ❌ "Deepgram API key not found"
**Solution**: Verify `DEEPGRAM_API_KEY` in .env file

### ❌ "Cannot connect to LiveKit"
**Solution**: 
- Check LiveKit server is running
- Try console mode first: `uv run python livekit_mcp_agent.py console`
- Verify LIVEKIT_URL is correct

### ❌ Airbnb search returns no results
**Solution**: 
- Ensure `--ignore-robots-txt` flag is in mcp_servers config
- Try broader location (e.g., "Paris" vs specific address)
- Check Node.js is properly installed

### ❌ First Airbnb search is very slow
**Normal**: npx downloads the package on first use (~10-30 seconds)

## Post-Setup

- [ ] Read QUICKSTART.md for usage examples
- [ ] Review AIRBNB_SETUP.md for detailed integration info
- [ ] Check SETUP_COMPLETE.md for customization options
- [ ] Star the LiveKit agents repo: https://github.com/livekit/agents
- [ ] Join LiveKit Discord for support: https://livekit.io/discord

## Production Checklist

- [ ] Replace local LiveKit with cloud instance
- [ ] Set up proper logging and monitoring
- [ ] Configure rate limiting
- [ ] Add error recovery mechanisms
- [ ] Test with real users
- [ ] Set up CI/CD pipeline
- [ ] Add health check endpoint
- [ ] Configure backup LLM provider
- [ ] Set up API key rotation
- [ ] Add usage analytics

## Optional Enhancements

- [ ] Add more MCP servers (weather, flights)
- [ ] Implement conversation history
- [ ] Add user authentication
- [ ] Create web interface
- [ ] Add multilingual support
- [ ] Implement voice selection
- [ ] Add booking confirmation flow
- [ ] Create mobile app integration

---

## 🎯 Quick Test Commands

```bash
# Install everything
uv sync

# Download models
uv run python livekit_mcp_agent.py download-files

# Test in console
uv run python livekit_mcp_agent.py console

# Test Airbnb MCP manually
npx -y @openbnb/mcp-server-airbnb --ignore-robots-txt

# Check Python packages
uv pip list | grep livekit

# Verify environment
type .env
```

## 📊 Success Criteria

Your setup is complete when:
- ✅ Agent starts without errors
- ✅ Voice input is recognized correctly
- ✅ LLM responds within 1-2 seconds
- ✅ Airbnb searches return valid results
- ✅ Voice output sounds natural
- ✅ End-to-end conversation flows smoothly

## 🚀 Ready to Launch!

Once all checks pass, you have a fully functional Airbnb travel voice agent!

Try this conversation:
```
You: "Hi there!"
Agent: "Hello! How can I help you today?"
You: "Find me a place to stay in Paris"
Agent: "I'd be happy to help you find a place in Paris!..."
```

**Congratulations!** 🎉
