import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Router
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from app.database import AsyncSessionLocal
from app.crud import (
    add_user_to_whitelist,
    is_user_whitelisted,
    get_whitelist,
    remove_user_from_whitelist,
    check_imei,
)
from app.config import settings
from app.crud import check_imei

logging.basicConfig(level=logging.INFO)

bot = Bot(token=settings.telegram_bot_token)
storage = MemoryStorage()
dp = Dispatcher()
# Создаем роутер
router = Router()

def create_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Добавить в белый список")],
            [KeyboardButton(text="Проверить белый список")],
            [KeyboardButton(text="Удалить из белого списка")],
            [KeyboardButton(text="Проверить IMEI")],
        ],
        resize_keyboard=True
    )
    return keyboard

async def check_user_whitelisted(user_id: int, db: AsyncSession):
    return await is_user_whitelisted(user_id, db)

async def user_only_handler(message: types.Message):
    user_id = message.from_user.id
    async with AsyncSessionLocal() as db:
        if not await check_user_whitelisted(user_id, db):
            await message.reply("Вы не в белом списке. Пожалуйста, добавьтесь в белый список.")
            return False
    return True

@router.message(Command("start"))
async def send_welcome(message: types.Message):
    user_id = message.from_user.id
    async with AsyncSessionLocal() as db:
        if await check_user_whitelisted(user_id, db):
            await message.reply(
                "Добро пожаловать! Выберите действие:",
                reply_markup=create_keyboard()
            )
        else:
            await message.reply("Вы не в белом списке. Пожалуйста, добавьтесь в белый список.")

@router.message(lambda message: message.text == "Добавить в белый список")
async def add_to_whitelist_handler(message: types.Message):
    user_id = message.from_user.id
    async with AsyncSessionLocal() as db:
        if await is_user_whitelisted(user_id, db):
            await message.reply("Вы уже в белом списке.")
        else:
            await add_user_to_whitelist(user_id, db)
            await message.reply("Вы добавлены в белый список.")

@router.message(lambda message: message.text == "Проверить белый список")
async def check_whitelist_handler(message: types.Message):
    user_id = message.from_user.id
    async with AsyncSessionLocal() as db:
        if await is_user_whitelisted(user_id, db):
            await message.reply("Вы в белом списке.")
        else:
            await message.reply("Вас нет в белом списке.")

@router.message(lambda message: message.text == "Удалить из белого списка")
async def remove_from_whitelist_handler(message: types.Message):
    user_id = message.from_user.id
    async with AsyncSessionLocal() as db:
        if await is_user_whitelisted(user_id, db):
            await remove_user_from_whitelist(user_id, db)
            await message.reply("Вы удалены из белого списка.")
        else:
            await message.reply("Вы не в белом списке.")

@router.message(lambda message: message.text == "Проверить IMEI")
async def check_imei_handler(message: types.Message):
    user_id = message.from_user.id
    if await user_only_handler(message):
        await message.reply("Введите IMEI для проверки:")

@router.message(lambda message: message.text.isdigit())
async def process_imei(message: types.Message):
    user_id = message.from_user.id
    if await user_only_handler(message):
        imei = message.text
        imei_info = await check_imei(imei)
        await message.reply(f"Результат проверки IMEI:\n{imei_info}")

# Подключаем роутер к диспетчеру
dp.include_router(router)

async def main():
    """Запуск бота."""
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
