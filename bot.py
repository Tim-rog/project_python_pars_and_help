from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command

from grq import *
from dtFrame import *


rtr = Router()


commands = ['start']


@rtr.message(Command('start'))
async def any(message: Message, state: FSMContext):
    await message.answer("Добро пожаловать", reply_markup=keyboard)

