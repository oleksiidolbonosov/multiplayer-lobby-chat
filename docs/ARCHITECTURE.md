# Architecture - Multiplayer Lobby + Realtime Chat Demo

Components:
- FastAPI API providing REST endpoints for lobby and chat, and WebSocket endpoint for realtime messages.
- Redis for ephemeral room state and message history; used for demo and later scaling.
- Unity client scripts showing how to create rooms, send chat messages and connect to WebSocket for live messages.

Scaling notes:
- For multiple API instances, use Redis pub/sub to propagate chat messages to all instances and use a centralized WebSocket gateway or sticky sessions.
