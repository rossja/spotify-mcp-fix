# spotify-mcp

A [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) server that connects Claude with Spotify. Control your Spotify playback, search music, manage playlists, and more -- all through natural conversation with Claude.

> **Fork Notice**: This project is forked from [varunneal/spotify-mcp](https://github.com/varunneal/spotify-mcp) and updated for the **Spotify Web API February 2026 changes**. Built and maintained with [Claude Code](https://claude.ai/claude-code).

## What's Changed (v0.4.0)

### Architecture Rewrite
- **Dropped `spotipy`** -- uses `httpx` async directly (native async, no `asyncio.to_thread` wrapping)
- **Single module** -- `server.py`, `spotify_api.py`, `utils.py` consolidated into one file
- **FastMCP** -- clean `@mcp.tool()` decorators instead of manual ToolModel + match/case routing
- **2 dependencies** -- only `mcp` + `httpx` (was `mcp` + `spotipy` + `python-dotenv`)
- **Explicit OAuth** -- `spotify-mcp --auth` for initial setup, auto-refresh on subsequent use

### Features (preserved from v0.3.0)
- Start, pause, and skip playback
- Search for tracks, albums, artists, and playlists
- Get detailed info about any Spotify item
- Manage the playback queue
- Full playlist CRUD (create, read, update, delete tracks)
- Retrieve liked/saved songs with optional genre enrichment
- Adapted for Spotify Feb 2026 API changes

## How It Works

```
Claude <--MCP (stdio)--> spotify-mcp <--httpx async--> Spotify Web API
```

1. Claude sends tool calls via the MCP protocol
2. The server translates them into Spotify Web API requests using `httpx`
3. OAuth tokens auto-refresh; initial auth via `spotify-mcp --auth`
4. Results are parsed into concise JSON and returned to Claude

### Available Tools

| Tool | Actions | Description |
|------|---------|-------------|
| `spotify_playback` | `get`, `start`, `pause`, `skip`, `previous` | Control music playback |
| `spotify_search` | -- | Search tracks, albums, artists, playlists |
| `spotify_queue` | `get`, `add` | View and manage play queue |
| `spotify_get_info` | -- | Get detailed item info by Spotify URI |
| `spotify_playlist` | `get`, `get_tracks`, `add_tracks`, `remove_tracks`, `change_details`, `create`, `delete` | Full playlist management |
| `spotify_liked_songs` | `get`, `get_with_genres` | Retrieve saved songs with optional genres |
| `spotify_recently_played` | -- | Get recently played tracks with timestamps |

### Architecture

```
src/spotify_mcp/
  __init__.py   # Entry point (stdio / --auth)
  server.py     # FastMCP server, API client, parsers — all in one
```

## Prerequisites

- **Python 3.12+**
- **Spotify Premium** account (required for Dev Mode API access since Feb 2026)
- **Spotify Developer App** credentials

## Configuration

### 1. Create Spotify Developer App

1. Go to [developer.spotify.com/dashboard](https://developer.spotify.com/dashboard)
2. Create a new app
3. Set redirect URI to `http://127.0.0.1:8080/callback`
4. Note your **Client ID** and **Client Secret**

> **Important (Feb 2026)**: Dev Mode apps are limited to 5 authorized users and require the app owner to have Spotify Premium.

### 2. Initial Authentication

Run the auth flow once to get your OAuth token:

```bash
SPOTIFY_CLIENT_ID=your_id SPOTIFY_CLIENT_SECRET=your_secret uv run spotify-mcp --auth
```

This opens a browser for Spotify login, then saves the token to `~/.spotify_mcp_cache.json`.

### 3. Add to MCP Client

#### Run locally (recommended)

```bash
git clone https://github.com/verIdyia/spotify-mcp.git
```

Add to your MCP config (Claude Desktop, Cursor, etc.):

```json
{
  "mcpServers": {
    "spotify": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/spotify-mcp",
        "run",
        "spotify-mcp"
      ],
      "env": {
        "SPOTIFY_CLIENT_ID": "your_client_id",
        "SPOTIFY_CLIENT_SECRET": "your_client_secret",
        "SPOTIFY_REDIRECT_URI": "http://127.0.0.1:8080/callback"
      }
    }
  }
}
```

#### Run with uvx

```json
{
  "mcpServers": {
    "spotify": {
      "command": "uvx",
      "args": [
        "--python", "3.12",
        "--from", "git+https://github.com/verIdyia/spotify-mcp",
        "spotify-mcp"
      ],
      "env": {
        "SPOTIFY_CLIENT_ID": "your_client_id",
        "SPOTIFY_CLIENT_SECRET": "your_client_secret",
        "SPOTIFY_REDIRECT_URI": "http://127.0.0.1:8080/callback"
      }
    }
  }
}
```

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `SPOTIFY_CLIENT_ID` | Yes | -- | Spotify app Client ID |
| `SPOTIFY_CLIENT_SECRET` | Yes | -- | Spotify app Client Secret |
| `SPOTIFY_REDIRECT_URI` | No | `http://127.0.0.1:8080/callback` | OAuth redirect URI |
| `SPOTIFY_CACHE_PATH` | No | `~/.spotify_mcp_cache.json` | Token cache file path |

## Troubleshooting

1. **First run**: Run `spotify-mcp --auth` to complete the OAuth flow before using with an MCP client
2. **Token expired**: Tokens auto-refresh. If issues persist, re-run `--auth`
3. **No active device**: Make sure Spotify is open and playing on at least one device
4. **Make sure `uv` is updated** -- version `>=0.54` recommended

### Debugging

Launch the MCP Inspector:

```bash
npx @modelcontextprotocol/inspector uv --directory /path/to/spotify-mcp run spotify-mcp
```

## Spotify API Feb 2026 Changes Summary

| Change | Impact | Status |
|--------|--------|--------|
| Search `limit` max reduced 50 -> 10 | Fewer results per search | Adapted |
| Playlist endpoints `/tracks` -> `/items` | Endpoint URLs changed | Adapted |
| Response field `tracks` -> `items` | Parsing updated | Adapted |
| Batch GET endpoints removed | Must fetch individually | Adapted |
| `popularity` field removed from tracks | No longer available | Handled |
| Dev Mode: 5 user limit, Premium required | Access restriction | Documented |

## Credits

- **Original project**: [varunneal/spotify-mcp](https://github.com/varunneal/spotify-mcp) by [Varun Srivastava](https://github.com/varunneal) (MIT License)
- **Original contributors**: @jamiew, @davidpadbury, @manncodes, @hyuma7, @aanurraj, @JJGO and others
- **Built with**: [httpx](https://github.com/encode/httpx), [MCP SDK](https://github.com/modelcontextprotocol/python-sdk)
- **Maintained with**: [Claude Code](https://claude.ai/claude-code) (Anthropic)

## License

MIT License -- see [LICENSE](LICENSE) for details.
