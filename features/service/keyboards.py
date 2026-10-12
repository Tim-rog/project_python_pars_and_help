from aiogram.enums import ButtonStyle
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from .callbacks import CATEGORY_LABELS, CategoryCb, WizardCb


def categories_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for category, label in CATEGORY_LABELS.items():
        kb.button(text=label, callback_data=CategoryCb(value=category))
    kb.button(
        text="✖️ Отмена",
        callback_data=WizardCb(action="cancel"),
        style=ButtonStyle.DANGER,
    )
    kb.adjust(2, 2, 2, 1, 1)
    return kb.as_markup()


def nav_kb(back: bool = True, skip: bool = False) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    if back:
        kb.button(text="Назад", callback_data=WizardCb(action="back"))
    if skip:
        kb.button(text="Пропустить", callback_data=WizardCb(action="skip"))
    kb.button(text="✖️ Отмена", callback_data=WizardCb(action="cancel"),
              style=ButtonStyle.DANGER)
    kb.adjust(2, 1)
    return kb.as_markup()