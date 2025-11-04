from fastapi import APIRouter
from app.core.config import settings
router = APIRouter()

@router.get("/ready")
async def ready():
    return {"status": "ready", "env": settings.APP_ENV}
