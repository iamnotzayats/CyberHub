from fastapi import APIRouter

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from database import database

from fastapi import FastAPI, HTTPException, status, Depends


v1_settings_router = APIRouter(prefix="/v1")

@v1_settings_router.get("/ping", tags=["health"])
async def ping_db(session: AsyncSession = Depends(database.get_session)):
    try:
        result = await session.execute(text("SELECT 1"))
        result.scalar_one()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database unavailable: {e}",
        )
    return {"status": "ok", "database": "alive"}