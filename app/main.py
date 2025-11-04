"""Multiplayer Lobby + Realtime Chat Demo - FastAPI app entrypoint"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.logger import setup_logging
from app.api import health, auth, lobby, chat, websocket

setup_logging()

app = FastAPI(
    title="Multiplayer Lobby + Realtime Chat Demo",
    version="0.1.0",
    description="Demo backend for lobby and realtime chat (WebSockets)."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/health", tags=["health"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(lobby.router, prefix="/lobby", tags=["lobby"])
app.include_router(chat.router, prefix="/chat", tags=["chat"])
app.include_router(websocket.router, prefix="/ws", tags=["ws"])
