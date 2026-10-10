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

from dtFrame import *


def taska(text):
    result = ''
    for i in text.split('.'):
        local = '\n'.join([f'{x.replace(";", "")}' for x in i.split(';')])
        result += f'*   \n{local}\n'
    return result


keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='add chat')]
    ],
    resize_keyboard=True)


class TaskForm(StatesGroup):
    waiting_chat = State()
    waiting_importance = State()


rtr = Router()


markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Delete'), InlineKeyboardButton(text='Redict')]
    ],
)


async def sparse(mess, bot):
    res = []
    print(''.join(''.join(mess.split(',')).split(' ')).split('@'))
    for x in ''.join(''.join(mess.split(',')).split(' ')).split('@'):
        print('wv', x)
        try:
            user = await bot.get_chat('@'+x)
            res.append(int(user.id))
        except Exception as e:
            print(e)
            continue
        print('mmm', int(user.id))
    return res


commands = ['add chat', 'start', '@', 'set']


async def our_filter(message: Message) -> bool:
    return len(message.text) > 3 and len(set(message.text)) > 3 and all([message.text not in x for x in commands]+[x not in message.text for x in commands])


@rtr.message(our_filter)
async def resent(message: Message, bot: Bot):
    for i in list(get_chats(message.chat.id)):
        await bot.send_message(i[0], message.text)


@rtr.message(Command('start'))
async def any(message: Message, state: FSMContext):
    await message.answer("Добро пожаловать", reply_markup=keyboard)


@rtr.message(Command('set'))
async def set_chat(message: Message):
    new = 0
    if message.chat.type in ('group', 'supergroup'):
        user = message.from_user.id
        chat = message.chat.id
        new = chats(user, chat)
    if new:
        await message.answer("Готово, теперь этот чат будет отслеживаться")


@rtr.message(TaskForm.waiting_chat, F.text.contains("@"))
async def adding(message: Message, state: FSMContext, bot:Bot):
    await state.clear()
    chats(message.from_user.id, await sparse(message.text, bot))
    print('bubu', await sparse(message.text, bot))
    await message.answer("Чаты добавленыны")



#
#
# @rtr.message(F.text == "New list")
# async def button1(message: Message, state: FSMContext):
#     await message.answer("Send your list")
#     await state.set_state(TaskForm.waiting_task)
#
#
# @rtr.message(F.text == "My lists")
# async def button1(message: Message, state: FSMContext):
#     await message.answer("твои таски: ")
#     dt = unleash(message.from_user.id)
#     for l, i in dt.iterrows():
#         await message.answer(taska(i['task']))
#
#
# @rtr.message(TaskForm.waiting_task)
# async def process_task(message: Message, state: FSMContext):
#     await message.answer(f"Твоя таска:\n {taska(message.text)}", reply_markup=markup)
#     create_list(message.from_user.id, message.text)
#     await state.clear()