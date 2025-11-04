from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict, Any
import uuid, json
from app.core.redis_client import get_redis

router = APIRouter()

class CreateRoomRequest(BaseModel):
    name: str = Field(..., description="Room display name")
    max_players: int = Field(4, ge=2, le=100)

def room_key(room_id: str) -> str:
    return f"room:{room_id}"

@router.post("/create")
async def create_room(req: CreateRoomRequest, redis=Depends(get_redis)):
    room_id = str(uuid.uuid4())
    room = {"id": room_id, "name": req.name, "max_players": req.max_players, "players": []}
    await redis.set(room_key(room_id), json.dumps(room))
    return room

@router.get("/list", response_model=List[Dict[str, Any]])
async def list_rooms(redis=Depends(get_redis)):
    keys = await redis.keys("room:*")
    rooms = []
    for k in keys:
        data = await redis.get(k)
        if data:
            rooms.append(json.loads(data))
    return rooms

class JoinRequest(BaseModel):
    player_id: str

@router.post("/{room_id}/join")
async def join_room(room_id: str, req: JoinRequest, redis=Depends(get_redis)):
    key = room_key(room_id)
    data = await redis.get(key)
    if not data:
        raise HTTPException(status_code=404, detail="Room not found")
    room = json.loads(data)
    if req.player_id in room['players']:
        return room
    if len(room['players']) >= room['max_players']:
        raise HTTPException(status_code=400, detail="Room is full")
    room['players'].append(req.player_id)
    await redis.set(key, json.dumps(room))
    return room

@router.post("/{room_id}/leave")
async def leave_room(room_id: str, req: JoinRequest, redis=Depends(get_redis)):
    key = room_key(room_id)
    data = await redis.get(key)
    if not data:
        raise HTTPException(status_code=404, detail="Room not found")
    room = json.loads(data)
    room['players'] = [p for p in room['players'] if p != req.player_id]
    await redis.set(key, json.dumps(room))
    return room
