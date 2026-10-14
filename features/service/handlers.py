from aiogram import F, Router, types
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, Message

from . import texts
from .callbacks import CategoryCb, PreviewCb, TermsCb, WizardCb
from .keyboards import categories_kb, nav_kb, photos_kb, preview_kb, terms_kb
from .screens import SCREENS
from .states import NewItem

router = Router(name="service")

ALL_FIELDS = {
    NewItem.category.state: "category",
    NewItem.title.state: "title",
    NewItem.description.state: "description",
    NewItem.photos.state: "photos",
    NewItem.terms.state: "terms",
    NewItem.place.state: "place",
}

TEXT_FIELDS = {
    NewItem.title.state: "title",
    NewItem.description.state: "description",
    NewItem.place.state: "place",
}

MAX_PHOTOS = 5

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
async def pick_category(callback: CallbackQuery, callback_data: CategoryCb, state: FSMContext):
    await state.update_data(category=callback_data.value)
    await process_step(callback.message, state, delete_msg=False)
    await callback.answer()


async def get_state_index(state: FSMContext) -> int:
    current = await state.get_state()
    states = NewItem.__states__
    idx = [s.state for s in states].index(current)

    return idx


def get_state_info(idx: int):
    state = NewItem.__states__[idx]
    text, make_kb = SCREENS[state.state]

    return state, text, make_kb


async def show_error(message: Message, state: FSMContext, error: str, question: str | None = None, kb=None):
    await message.delete()
    message_id = await state.get_value("wizard_msg_id")
    idx = await get_state_index(state)
    if question is None:
        _, question, make_kb = get_state_info(idx)
        kb = make_kb()
    await message.bot.edit_message_text(text=texts.step(idx + 1, f"{question}\n\n⚠️ {error}"),
                                        chat_id=message.chat.id,
                                        message_id=message_id,
                                        reply_markup=kb,
                                        )


async def send_card(message: types.Message, state: FSMContext, text: str, send_photos: bool = False, 
                    kb: InlineKeyboardMarkup | None = None):
    photos = list(await state.get_value("photos") or [])
    old_id = await state.get_value("wizard_msg_id")

    if photos and send_photos:
        msg = await message.answer_photo(photos[0], caption=text, reply_markup=kb)
    else:
        msg = await message.answer(text, reply_markup=kb)

    await state.update_data(wizard_msg_id=msg.message_id)
    
    try:
        await message.bot.delete_message(message.chat.id, old_id)
    except TelegramBadRequest:
        pass


@router.callback_query(NewItem.preview, PreviewCb.filter(F.action == "publish"))
async def publish_button(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    title = await state.get_value("title")

    # TODO: сохранить объявление в базу данных

    msg = callback.message
    if msg.photo:
        await msg.edit_caption(caption=texts.published(title), reply_markup=None)
    else:
        await msg.edit_text(texts.published(title), reply_markup=None)

    await state.clear()


async def process_step(message: types.Message, state: FSMContext, delete_msg: bool = True):
    message_id = await state.get_value("wizard_msg_id")
    idx = await get_state_index(state)
    next_state = NewItem.__states__[idx + 1]

    if next_state == NewItem.preview:
        data = await state.get_data()

        photos = data["photos"] or []
        text = texts.item_preview(data)
        
        await state.set_state(next_state)
        await send_card(message, state, text, photos, preview_kb())

        return

    _, text, markup = get_state_info(idx + 1)


    await message.bot.edit_message_text(text=texts.step(idx + 2, text),
                                        chat_id=message.chat.id,
                                        message_id=message_id,
                                        reply_markup=markup(),
                                        )
    await state.set_state(next_state)

    if delete_msg:
        await message.delete()


@router.message(StateFilter(*TEXT_FIELDS), F.text)
async def process_text(message: types.Message, state: FSMContext):
    field = ALL_FIELDS[await state.get_state()]
    await state.update_data({field: message.text})
    await process_step(message=message, state=state)


@router.message(StateFilter(*TEXT_FIELDS), ~F.text)
async def need_text(message: types.Message, state: FSMContext):
    await show_error(message, state, texts.TEXT_NEEDED)


@router.message(StateFilter(NewItem.photos), F.photo)
async def process_photo(message: types.Message, state: FSMContext):
    photos = list(await state.get_value("photos") or [])
    await message.delete()

    if len(photos) >= MAX_PHOTOS:
        # TODO: при достижении максимального количества фоток бот просто молчит
        # TODO: можно оставить так, либо придумать как говорить об этом пользователю
        # TODO: уже есть функция show_error, но она не подойдёт т.к. делает лишние действия, но можно её переписать
        return

    photos.append(message.photo[-1].file_id)
    await state.update_data(photos=photos)

    kb = photos_kb() if len(photos) == 0 else photos_kb(has_photos=True)

    idx = await get_state_index(state)
    text = f"{texts.ASK_PHOTOS}\n\n📎 Загружено: {len(photos)}/{MAX_PHOTOS}"

    await message.bot.edit_message_text(text=texts.step(idx + 1, text),
                                        message_id=await state.get_value("wizard_msg_id"),
                                        chat_id=message.chat.id,
                                        reply_markup=kb
                                        )


@router.callback_query(NewItem.photos, WizardCb.filter(F.action == "done"))
async def photos_done(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await process_step(callback.message, state, delete_msg=False)


@router.message(StateFilter(NewItem.photos), ~F.photo)
async def need_photo(message: types.Message, state: FSMContext):
    await show_error(message, state, texts.PHOTO_NEEDED)


@router.callback_query(NewItem.terms, TermsCb.filter())
async def pick_terms(callback: CallbackQuery, callback_data: TermsCb,  state: FSMContext):
    await state.update_data(terms=callback_data.value)
    await callback.answer()

    if callback_data.value == "free":
        await process_step(message=callback.message, state=state, delete_msg=False)
        return

    text = {"exchange": texts.ASK_TRADE, "price": texts.ASK_PRICE}.get(callback_data.value)
    await callback.message.edit_text(texts.step(await get_state_index(state) + 1, text), reply_markup=nav_kb(back=True))


@router.message(NewItem.terms, F.text)
async def terms_text(message: Message, state: FSMContext):
    # TODO: если юзер два раза подряд введёт неправильную строку, то телеграм выкинет ошибку TelegramBadRequest
    # TODO: message is not modified: specified new message content and reply markup are exactly the same
    # TODO: нужно сделать функцию save_edit, которая будет ловить эту ошибку через try except, т.к. это сильно
    # TODO: засоряет консоль
    terms = await state.get_value("terms")
    if terms is None or terms == "free":
        return
        return

    if terms == "price":
        raw = message.text.replace(" ", "").replace("₽", "").replace("р", "")
        if not raw.isdigit() or not (0 < int(raw) <= 1_000_000):
            await show_error(message, state, texts.INVALID_PRICE, texts.ASK_PRICE, nav_kb(back=True))
            return

        await state.update_data({terms: int(raw)})
    else:
        await state.update_data({terms: message.text})

    await process_step(message=message, state=state)


@router.callback_query(StateFilter(NewItem), WizardCb.filter(F.action == "back"))
async def wizard_back(callback: CallbackQuery, state: FSMContext):
    idx = await get_state_index(state)
    current_state = await state.get_state()

    if idx == 0:
        await callback.answer("Это первый шаг")
        return

    # нужно, чтобы кнопка "назад" возвращала на предыдущий шаг, если пользователь выбрал "Обмен" или "Цена" и захотел
    # вернуться назад
    if current_state == NewItem.terms.state and await state.get_value("terms"):
        await state.update_data(terms=None)
        await send_card(message=callback.message, state=state, text=texts.item_preview(await state.get_data()),)
        await callback.message.edit_text(texts.step(idx + 1, texts.ASK_TERMS), reply_markup=terms_kb())
        await callback.answer()
        return

    prev, text, make_kb = get_state_info(idx - 1)
    await state.set_state(prev)

    # если юзер возвращается до условий или фоток - сбрасываем их
    if prev == NewItem.terms.state:
        await state.update_data(terms=None)
    if prev == NewItem.photos.state:
        await state.update_data(photos=[])

    # если юзер на шаге "превью" и хочет вернуться назад, нужно присылать новое сообщение вместо редактирования,
    # т.к. старое с вложенными фотками редактировать нельзя. Ограничение телеграма
    if current_state == NewItem.preview.state:
        await send_card(callback.message, state, texts.step(idx, text), kb=make_kb())
    else:
        await callback.message.edit_text(texts.step(idx, text), reply_markup=make_kb())

    await callback.answer()


@router.callback_query(StateFilter(NewItem), WizardCb.filter(F.action == "skip"))
async def wizard_skip(callback: CallbackQuery, state: FSMContext):
    field = ALL_FIELDS[await state.get_state()]

    await state.update_data({field: None})
    await process_step(message=callback.message, state=state, delete_msg=False)
    await callback.answer()


@router.callback_query(StateFilter(NewItem), WizardCb.filter(F.action == "cancel"))
async def wizard_cancel(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(texts.ACTION_CANCELED)
    await callback.answer()
