from aiogram.enums import ButtonStyle
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from .callbacks import CATEGORY_LABELS, CategoryCb, WizardCb, TermsCb


def categories_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for category, label in CATEGORY_LABELS.items():
        kb.button(text=label, callback_data=CategoryCb(value=category))
    kb.button(
        text="Отмена",
        callback_data=WizardCb(action="cancel"),
        style=ButtonStyle.DANGER,
    )
    kb.adjust(2, 2, 2, 1, 1)
    return kb.as_markup()


def nav_builder(back: bool = True, skip: bool = False) -> InlineKeyboardBuilder:
    kb = InlineKeyboardBuilder()
    if back:
        kb.button(text="Назад", callback_data=WizardCb(action="back"))
    if skip:
        kb.button(text="Пропустить", callback_data=WizardCb(action="skip"))
    kb.button(text="Отмена", callback_data=WizardCb(action="cancel"),
              style=ButtonStyle.DANGER)
    kb.adjust(2, 1)
    return kb


def nav_kb(back: bool = True, skip: bool = False) -> InlineKeyboardMarkup:
    return nav_builder(back, skip).as_markup()


def photos_kb(has_photos: bool = False) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()

    if has_photos:
        kb.button(text="Готово", callback_data=WizardCb(action="done"))
    kb.attach(nav_builder(back=True, skip=not has_photos))

    return kb.as_markup()


def terms_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="Бесплатно", callback_data=TermsCb(value="free"))
    kb.button(text="Обмен", callback_data=TermsCb(value="exchange"))
    kb.button(text="Цена", callback_data=TermsCb(value="price"))
    kb.adjust(3)

    kb.attach(nav_builder())

    return kb.as_markup()