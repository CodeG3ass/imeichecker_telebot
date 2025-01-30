from fastapi import Header, HTTPException
from app.config import settings

async def get_api_token(authorization: str = Header(...)):
    if authorization != f"Bearer {settings.api_auth_token}":
        raise HTTPException(status_code=403, detail="Invalid token")
    return authorization