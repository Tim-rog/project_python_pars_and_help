import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand

from bot import rtr as tasks_router
from bot import *


async def commands(bot: Bot):
    commands = [BotCommand(command='start', description='/start'),
                BotCommand(command='set', description='/set')]
    await bot.set_my_commands(commands)


async def main():
    storage = MemoryStorage()
    bot = Bot(token="8937550208:AAFhsjwCyKtncwiTILwBmyBXMxtDb_fYDhw")
    dp = Dispatcher(storage=storage)

    dp.include_router(tasks_router)

    print("Бот запущен")
    await dp.start_polling(bot)
    await FSMContext.set_state(TaskForm.waiting_importance)

if __name__ == "__main__":
    asyncio.run(main())