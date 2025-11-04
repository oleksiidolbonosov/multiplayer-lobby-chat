from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict, List, Any
import asyncio, json
from app.core.redis_client import get_redis

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active: Dict[str, List[WebSocket]] = {}
        self.lock = asyncio.Lock()

    async def connect(self, room_id: str, websocket: WebSocket):
        await websocket.accept()
        async with self.lock:
            self.active.setdefault(room_id, []).append(websocket)

    async def disconnect(self, room_id: str, websocket: WebSocket):
        async with self.lock:
            conns = self.active.get(room_id, [])
            if websocket in conns:
                conns.remove(websocket)

    async def broadcast(self, room_id: str, message: Any):
        conns = list(self.active.get(room_id, []))
        for ws in conns:
            try:
                await ws.send_json(message)
            except Exception:
                pass

manager = ConnectionManager()

@router.websocket("/rooms/{room_id}")
async def ws_room(websocket: WebSocket, room_id: str):
    await manager.connect(room_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Echo back as JSON
            await manager.broadcast(room_id, {"echo": data})
    except WebSocketDisconnect:
        await manager.disconnect(room_id, websocket)