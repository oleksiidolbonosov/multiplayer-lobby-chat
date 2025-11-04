# Multiplayer Lobby + Realtime Chat Demo

Production-minded demo: **Multiplayer Lobby + Realtime Chat** built with FastAPI (backend) and Unity (client).

Features:
- Lobby: create/list/join/leave rooms (ephemeral state in Redis)
- Realtime chat in rooms via WebSockets
- Unity client examples (Lobby + Chat + WebSocket subscription)
- Docker Compose stack (redis + api)
- CI workflow for tests
- Simple tests and developer docs

This demo is intentionally compact so you can run it locally quickly and show a live demo during interviews or investor meetings.

## Quickstart

```bash
# build & run via docker-compose (requires Docker & docker-compose)
docker-compose up --build

# Open API docs: http://localhost:8000/docs
# Unity: import UnityClient folder into a Unity project and attach scripts to GameObjects
```

See `docs/` for architecture, demo script and talking points.
