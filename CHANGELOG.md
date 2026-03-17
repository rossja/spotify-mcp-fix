# Changelog

## [0.4.0] - 2026-03-17

### Architecture Rewrite
- **Dropped `spotipy` dependency** -- uses `httpx` async directly for all Spotify API calls
- **Dropped `python-dotenv` dependency** -- env vars are passed via MCP client config
- **Consolidated to single module** -- merged `server.py`, `spotify_api.py`, `utils.py` into one file
- **Switched to FastMCP** -- uses `@mcp.tool()` decorators instead of low-level Server API + ToolModel pattern
- **Native async throughout** -- no more `asyncio.to_thread()` wrapping blocking calls
- **Parallel genre fetching** -- `asyncio.gather` with semaphore instead of `ThreadPoolExecutor`
- **Shared `httpx.AsyncClient`** -- connection pooling across all API calls
- **Explicit OAuth flow** -- `spotify-mcp --auth` for initial token setup, auto-refresh on use
- **Token cache** -- defaults to `~/.spotify_mcp_cache.json`, configurable via `SPOTIFY_CACHE_PATH`

### Improvements
- Cleaner error handling with user-friendly messages for common HTTP errors
- Device auto-selection for playback (picks first available if none active)
- Reduced total dependencies from 3 to 2 (mcp + httpx)

## [0.3.0] - 2026-02-28

### Spotify API Feb 2026 Migration
- Adapted search limit to max 10 (Spotify Dev Mode restriction)
- Migrated playlist endpoints from `/tracks` to `/items`
- Added response field compatibility for both old and new API formats
- Replaced removed batch artist endpoint with parallel individual fetches
- Updated playlist creation to use `POST /me/playlists`

### New Features
- Added playlist `delete` action (unfollow/delete via `DELETE /playlists/{id}/followers`)
- Lazy client initialization -- server starts without credentials, client created on first tool call

### Bug Fixes
- Replaced `assert` with proper error handling for unknown tool names
- Fixed `change_playlist_details()` missing return value
- Fixed `get_liked_songs()` limit edge case (stops immediately when limit reached)
- Added null track handling in liked songs pagination

### Improvements
- Aligned search default limit with Spotify's new default (5)
- Expanded `.gitignore` for better coverage
- Removed Korean comments for international audience
- Added `.env.example` for easier setup
- Updated documentation with Feb 2026 API changes

### Security
- Ensured OAuth token cache is excluded from repository
- No credentials or tokens in committed files

## [0.2.0] - Upstream

Original release from [varunneal/spotify-mcp](https://github.com/varunneal/spotify-mcp).
See upstream repository for full history.
