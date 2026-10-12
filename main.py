import os
import asyncio

from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode

from features.service import router as service_router
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand

from dotenv import load_dotenv

load_dotenv()
bot_token_raw = os.getenv('BOT_TOKEN')

if bot_token_raw is None:
    raise ValueError("BOT_TOKEN не задан в переменных окружения.")

BOT_TOKEN: str = bot_token_raw


async def set_commands(bot: Bot):
    bot_commands = [BotCommand(command='start', description='/start')]
    await bot.set_my_commands(bot_commands)


async def main():
    session = AiohttpSession()

    bot = Bot(token=BOT_TOKEN, session=session, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(service_router)

    dp.startup.register(set_commands)

    print("Бот запущен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
