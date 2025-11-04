from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import List
from app.core.redis_client import get_redis
import json, asyncio

router = APIRouter()

class ChatMessage(BaseModel):
    room_id: str
    sender: str
    message: str

@router.post("/send")
async def send_message(msg: ChatMessage, redis=Depends(get_redis)):
    channel = f"chat:room:{msg.room_id}"
    payload = {"sender": msg.sender, "message": msg.message, "ts": asyncio.get_event_loop().time()}
    # publish to channel (other instances can subscribe)
    await redis.publish(channel, json.dumps(payload))
    # store in history (LPUSH capped list)
    key = f"chat_history:{msg.room_id}"
    await redis.lpush(key, json.dumps(payload))
    await redis.ltrim(key, 0, 99)  # keep last 100 messages
    return {"ok": True}

@router.get("/history/{room_id}", response_model=List[dict])
async def history(room_id: str, redis=Depends(get_redis)):
    key = f"chat_history:{room_id}"
    items = await redis.lrange(key, 0, -1)
    return [json.loads(i) for i in items]