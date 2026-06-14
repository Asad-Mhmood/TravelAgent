# Airbnb MCP Server Integration Guide

This guide explains how the Airbnb MCP server is integrated with your LiveKit voice agent.

## Overview

The voice agent uses the [openbnb-org/mcp-server-airbnb](https://github.com/openbnb-org/mcp-server-airbnb) MCP server to enable Airbnb vacation rental search capabilities through natural voice conversations.

## Features

### 🔍 Search Capabilities
- **Location-based search** - Search by city, state, region, or country
- **Date filtering** - Specify check-in and check-out dates
- **Guest configuration** - Adults, children, infants, and pets
- **Price range** - Set minimum and maximum price per night
- **Property types** - Filter by entire home, private room, shared room, or hotel room
- **Pagination** - Browse through multiple pages of results

### 🏠 Property Details
- Comprehensive listing information
- Amenities and facilities
- House rules and policies
- Location with coordinates
- Direct booking links

## Prerequisites

1. **Node.js 18+** - Required to run the Airbnb MCP server via `npx`
   - Check if installed: `node --version`
   - Download from: https://nodejs.org/

2. **Python dependencies** - Already included in `pyproject.toml`
   - `livekit-agents[mcp]` - MCP support for LiveKit

## How It Works

### Architecture

```
┌─────────────┐
│ Voice Agent │
└──────┬──────┘
       │
       ▼
┌─────────────┐        ┌──────────────┐
│ MCP Client  │───────▶│ Airbnb MCP   │
│ (LiveKit)   │        │ Server (npx) │
└─────────────┘        └──────┬───────┘
                              │
                              ▼
                       ┌──────────────┐
                       │ Airbnb.com   │
                       │ (Web Scrape) │
                       └──────────────┘
```

### Configuration

The Airbnb MCP server is configured in `livekit_mcp_agent.py`:

```python
mcp_servers=[
    mcp.MCPServerStdio(
        name="airbnb",
        command="npx",
        args=["-y", "@openbnb/mcp-server-airbnb", "--ignore-robots-txt"],
    ),
]
```

**Configuration Details:**
- `name`: Identifier for the MCP server
- `command`: `npx` - Node Package Executor
- `args`:
  - `-y` - Automatically confirm installation
  - `@openbnb/mcp-server-airbnb` - NPM package name
  - `--ignore-robots-txt` - Bypass robots.txt restrictions (required for functionality)

## Available Tools

### 1. airbnb_search

Search for Airbnb listings with advanced filtering.

**Parameters:**
- `location` (required) - e.g., "San Francisco, CA" or "Paris, France"
- `checkin` (optional) - Check-in date (YYYY-MM-DD)
- `checkout` (optional) - Check-out date (YYYY-MM-DD)
- `adults` (optional) - Number of adults (default: 1)
- `children` (optional) - Number of children (default: 0)
- `infants` (optional) - Number of infants (default: 0)
- `pets` (optional) - Number of pets (default: 0)
- `minPrice` (optional) - Minimum price per night
- `maxPrice` (optional) - Maximum price per night
- `propertyType` (optional) - `entire_home`, `private_room`, `shared_room`, `hotel_room`
- `cursor` (optional) - Pagination cursor
- `ignoreRobotsText` (optional) - Set to `true` (recommended)

**Example Voice Commands:**
- "Find me a place to stay in Tokyo for 2 adults next week"
- "Search for pet-friendly apartments in Miami under $150 per night"
- "Show me entire homes in London from March 15 to March 20"

### 2. airbnb_listing_details

Get detailed information about a specific property.

**Parameters:**
- `id` (required) - Airbnb listing ID
- `checkin` (optional) - Check-in date (YYYY-MM-DD)
- `checkout` (optional) - Check-out date (YYYY-MM-DD)
- `adults` (optional) - Number of adults
- `children` (optional) - Number of children
- `infants` (optional) - Number of infants
- `pets` (optional) - Number of pets
- `ignoreRobotsText` (optional) - Set to `true` (recommended)

**Example Voice Commands:**
- "Tell me more about listing 12345678"
- "What amenities does this property have?"
- "Show me the house rules for this listing"

## Testing

### Console Mode Test

Test the integration locally without needing a LiveKit server:

```bash
# Download required models first
uv run python livekit_mcp_agent.py download-files

# Run in console mode
uv run python livekit_mcp_agent.py console
```

### Test Conversation Flow

1. Start the agent in console mode
2. Wait for the greeting
3. Try these test queries:
   - "Find me an apartment in San Francisco"
   - "Search for a beach house in Miami for 2 adults and 2 children"
   - "Show me properties in New York under $200 per night"

## Troubleshooting

### Node.js Not Found

**Error:** `Command 'npx' not found`

**Solution:**
1. Install Node.js 18+ from https://nodejs.org/
2. Verify installation: `node --version` and `npx --version`
3. Restart your terminal
4. Try running the agent again

### MCP Server Connection Failed

**Error:** MCP server fails to start or connect

**Solution:**
1. Check Node.js is installed: `node --version`
2. Test the MCP server manually:
   ```bash
   npx -y @openbnb/mcp-server-airbnb --ignore-robots-txt
   ```
3. Check for firewall or antivirus blocking npx
4. Clear npx cache: `npx clear-npx-cache`

### No Search Results

**Issue:** Airbnb search returns empty results

**Solutions:**
1. Ensure `ignoreRobotsText` is set to `true` in tool calls
2. Try a broader location (e.g., "Paris" instead of specific address)
3. Remove date filters to test if dates are causing issues
4. Check the agent instructions include the robots.txt override

### Slow First Request

**Issue:** First search takes a long time

**Explanation:** This is normal - `npx` downloads and caches the MCP server package on first use. Subsequent requests will be much faster.

## Customization

### Modify Agent Instructions

Edit the `Assistant` class in `livekit_mcp_agent.py`:

```python
def __init__(self):
    super().__init__(
        instructions="""Your custom instructions here...
        
        Remember to set ignoreRobotsText to true for Airbnb tools."""
    )
```

### Add More MCP Servers

You can add additional MCP servers alongside Airbnb:

```python
mcp_servers=[
    # Airbnb
    mcp.MCPServerStdio(
        name="airbnb",
        command="npx",
        args=["-y", "@openbnb/mcp-server-airbnb", "--ignore-robots-txt"],
    ),
    # Add another stdio-based server
    mcp.MCPServerStdio(
        name="another-server",
        command="npx",
        args=["-y", "another-mcp-package"],
    ),
    # Or add an HTTP-based server
    mcp.MCPServerHTTP(url="http://localhost:8089/mcp"),
]
```

## Security & Compliance

### Robots.txt Override

The `--ignore-robots-txt` flag is used because:
1. Airbnb's robots.txt blocks automated access
2. The server respects rate limits and makes reasonable requests
3. It only accesses publicly available listing information
4. This is for legitimate vacation rental search assistance

### Data Usage

- The MCP server only retrieves publicly visible information
- No user credentials or personal data are stored
- All searches are anonymous from the agent's perspective
- Booking still requires the user to visit Airbnb's website

### Rate Limiting

The MCP server implements respectful rate limiting:
- Request timeouts to prevent hanging
- Reasonable delays between requests
- No aggressive scraping or bulk downloads

## Alternative: Hosted Solution

If you don't want to run the MCP server locally, consider:

**[openbnb.ai](https://openbnb.ai/)** - Hosted MCP server with:
- Zero setup required
- Advanced filters and UI components
- Managed and maintained service
- No Node.js installation needed

## Resources

- **MCP Server GitHub**: https://github.com/openbnb-org/mcp-server-airbnb
- **LiveKit Agents Docs**: https://docs.livekit.io/agents/
- **MCP Protocol**: https://modelcontextprotocol.io/
- **Node.js Download**: https://nodejs.org/

## Support

For issues specific to:
- **Airbnb MCP Server**: https://github.com/openbnb-org/mcp-server-airbnb/issues
- **LiveKit Agents**: https://github.com/livekit/agents/issues
- **This Integration**: Create an issue in your repository

---

**Note**: This integration is not affiliated with Airbnb, Inc. It uses publicly available information for legitimate vacation rental search assistance.
