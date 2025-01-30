import httpx
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import User
from app.config import settings

async def check_imei(imei: str):
    url = "https://api.imeicheck.net/v1/checks"
    headers = {
        "Authorization": f"Bearer {settings.imeicheck_api_key}",
        "Accept-Language": "en"
    }
    data = {
        "deviceId": imei,
        "serviceId": 12
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=data)
        return response.json()

# Функция для проверки, есть ли пользователь в белом списке
async def is_user_whitelisted(user_id: int, db: AsyncSession) -> bool:
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none() is not None

# Функция для получения белого списка
async def get_whitelist(db: AsyncSession):
    result = await db.execute(select(User))
    return result.scalars().all()

# Функция для удаления пользователя из белого списка
async def remove_user_from_whitelist(user_id: int, db: AsyncSession):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if user:
        await db.delete(user)
        await db.commit()

# Функция для добавления пользователя в белый список
async def add_user_to_whitelist(user_id: int, db: AsyncSession):
    user = User(id=user_id)
    db.add(user)
    await db.commit()
