from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from states import *
from asyncio import *
from aiogram.fsm.state import State, StatesGroup
from aiogram import Bot, Dispatcher
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import StateFilter
from aiogram.filters import Command
from aiogram.types import ChatMemberUpdated
from aiogram.filters import IS_MEMBER, IS_NOT_MEMBER, ChatMemberUpdatedFilter

from grq import *
from dtFrame import *


keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='add chat')]
    ],
    resize_keyboard=True)


rtr = Router()


#Временно не нужно
markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Delete'), InlineKeyboardButton(text='Redict')]
    ],
)

commands = ['add chat', 'start', '@', 'set']
i_mess = 8
j_mess = 5


async def our_filter(message: Message) -> bool:
    '''Фильтр, который проверяет, что длина сообщения больше i, и в сообщение использованно больше j различных символов.
    А также, смотрит, чтобы сообщение не совпадало с командамиц'''
    if message.text is None:
        return False
    return len(message.text) > i_mess and len(set(message.text)) > j_mess and all([message.text not in x for x in commands]+[x not in message.text for x in commands])


@rtr.message(our_filter)
async def resent(message: Message, bot: Bot):
    '''Читает осмысленные сообщения в чате, затем возрващает'''
    print(await classify(message.text))
    importance = await classify(message.text)
    if importance == 'IMPORTANT':
        for i in list(get_chats(message.chat.id)):
            if i[0] != message.from_user.id:
                await bot.send_message(i[0], f'От: @{message.from_user.username}\n\n{message.text}')


@rtr.message(Command('start'))
async def any(message: Message):
    await message.answer("Добро пожаловать", reply_markup=keyboard)


@rtr.message(Command('set'))
async def set_chat(message: Message):
    if message.chat.type in ('group', 'supergroup'):
        user = message.from_user.id
        chat = message.chat.id
        if not in_chats(user, chat):
            add_chat(user, chat)
            await message.answer("Готово, теперь этот чат будет отслеживаться")


@rtr.message(Command('deset'))
async def de_set_chat(message: Message):
    if message.chat.type in ('group', 'supergroup'):
        user = message.from_user.id
        chat = message.chat.id
        if in_chats(user, chat):
            del_chat(user, chat)
            await message.answer("Этот чат больше не будет отслеживаться")

