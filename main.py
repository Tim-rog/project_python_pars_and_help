import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand

from bot import rtr as tasks_router
from bot import *


tokeen = open('venv/secrets.env').readlines()[1]


async def commands(bot: Bot):
    commands = [BotCommand(command='start', description='/start'),
                BotCommand(command='set', description='/set'),
                BotCommand(command='deset', description='/deset')]
    await bot.set_my_commands(commands)


async def main():
    storage = MemoryStorage()
    bot = Bot(token=tokeen)
    dp = Dispatcher(storage=storage)

    dp.include_router(tasks_router)

    print("Бот запущен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())