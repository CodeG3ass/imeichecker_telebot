from fastapi import FastAPI
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import IMEIRequest, IMEIResponse
from app.database import AsyncSessionLocal, startup, shutdown
from app.crud import (
    check_imei,
    is_user_whitelisted,
    add_user_to_whitelist,
    get_whitelist,
    remove_user_from_whitelist,
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Инициализация базы данных при старте
@app.on_event("startup")
async def on_startup():
    await startup()

# Закрытие соединений при завершении
@app.on_event("shutdown")
async def on_shutdown():
    await shutdown()

# Зависимость для получения асинхронной сессии
async def get_db():
    async with AsyncSessionLocal() as db:
        yield db

@app.post("/api/check-imei", response_model=IMEIResponse)
async def api_check_imei(request: IMEIRequest):
    result = await check_imei(request.imei)
    return {"status": "success", "data": result}

# Зависимость для получения асинхронной сессии
async def get_db():
    async with AsyncSessionLocal() as db:
        yield db

# Эндпоинты
@app.post("/add-to-whitelist/{user_id}")
async def add_to_whitelist(user_id: int, db: AsyncSession = Depends(get_db)):
    await add_user_to_whitelist(user_id, db)
    return {"message": f"User {user_id} added to whitelist"}

@app.get("/check-whitelist/{user_id}")
async def check_whitelist(user_id: int, db: AsyncSession = Depends(get_db)):
    if await is_user_whitelisted(user_id, db):
        return {"message": f"User {user_id} is whitelisted"}
    else:
        raise HTTPException(status_code=404, detail="User not found in whitelist")

@app.get("/get-whitelist")
async def get_whitelist_endpoint(db: AsyncSession = Depends(get_db)):
    whitelist = await get_whitelist(db)
    return {"whitelist": [user.id for user in whitelist]}

@app.delete("/remove-from-whitelist/{user_id}")
async def remove_from_whitelist(user_id: int, db: AsyncSession = Depends(get_db)):
    await remove_user_from_whitelist(user_id, db)
    return {"message": f"User {user_id} removed from whitelist"}

@app.get("/")
async def root():
    return {"message": "IMEI Checker API is running"}