from aiogram.fsm.state import State, StatesGroup


class NewItem(StatesGroup):
    category = State()
    title = State()
    description = State()
    photos = State()