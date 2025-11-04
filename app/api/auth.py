from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import jwt
from app.core.config import settings

router = APIRouter()

class TokenRequest(BaseModel):
    player_id: str

@router.post("/token")
async def create_token(req: TokenRequest):
    exp = datetime.utcnow() + timedelta(hours=8)
    payload = {"sub": req.player_id, "exp": exp.timestamp()}
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    return {"access_token": token, "token_type": "bearer"}

@router.get("/token")
async def get_token():
    return {"token": "demo-token", "player_id": "player_" + str(hash("demo") % 10000)}