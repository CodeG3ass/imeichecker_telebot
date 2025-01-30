from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.models import Base

# Логгирование пути к базе данных
print(f"Database path: {settings.db_path}")

# Инициализация асинхронного движка
engine = create_async_engine(settings.db_path, echo=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Инициализация базы данных
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Инициализация базы данных при старте приложения
async def startup():
    await init_db()

# Закрытие соединений при завершении
async def shutdown():
    await engine.dispose()