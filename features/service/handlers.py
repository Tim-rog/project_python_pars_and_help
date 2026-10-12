from aiogram import Bot, F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from . import texts
from .callbacks import CategoryCb, WizardCb
from .keyboards import categories_kb, nav_kb
from .screens import SCREENS
from .states import NewItem
router = Router(name="service")


# @router.message(Command("open"))
# async def open_shop(message: Message):
#     builder = InlineKeyboardBuilder()
#
#     builder.button(text="📦 Барахолка", callback_data="btn_like")
#     builder.button(text="➕ Разместить", callback_data="btn_dislike")
#     builder.button(text="🔎 Бюро находок", callback_data="btn_dislike")
#     builder.button(text="🗂 Мои объявления", callback_data="btn_dislike")
#
#     builder.adjust(2, 2)
#
#     await message.answer("🎒 Барахолка и бюро находок МАИ\n\n"
#                          "Отдавай ненужное, находи нужное,\nвозвращай потерянное.\n",
#                          reply_markup=builder.as_markup())

@router.message(Command("new"))
async def new_item(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(NewItem.category)
    msg = await message.answer(texts.step(1, texts.ASK_CATEGORY), reply_markup=categories_kb())

    await state.update_data(wizard_msg_id=msg.message_id)


@router.callback_query(NewItem.category, CategoryCb.filter())
async def pick_category(callback: CallbackQuery, callback_data: CategoryCb,
                        state: FSMContext):
    await state.update_data(category=callback_data.value)
    await state.set_state(NewItem.title)
    await callback.message.edit_text(texts.step(2, texts.ASK_TITLE), reply_markup=nav_kb())
    await callback.answer()


@router.message(NewItem.title, F.text)
async def process_title(message: types.Message, state: FSMContext):
    await state.update_data(title=message.text)
    await state.set_state(NewItem.photos)
    message_id = await state.get_value("wizard_msg_id")
    await message.bot.edit_message_text(text=texts.step(3, "test"),
                                        chat_id=message.chat.id,
                                        message_id=message_id,
                                        reply_markup=nav_kb()
    )


@router.callback_query(WizardCb.filter(F.action == "back"))
async def wizard_back(callback: CallbackQuery, state: FSMContext):
    current = await state.get_state()
    states = NewItem.__states__
    idx = [s.state for s in states].index(current)

    if idx == 0:
        await callback.answer("Это первый шаг")
        return

    prev = states[idx - 1]
    await state.set_state(prev)
    text, make_kb = SCREENS[prev.state]
    await callback.message.edit_text(texts.step(idx, text), reply_markup=make_kb())
    await callback.answer()


@router.callback_query(WizardCb.filter(F.action == "cancel"))
async def wizard_cancel(callback: CallbackQuery, callback_data: CategoryCb, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(texts.ACTION_CANCELED)
    await callback.answer()


