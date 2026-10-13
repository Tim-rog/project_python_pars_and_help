from enum import Enum

from aiogram.filters.callback_data import CallbackData


class Category(str, Enum):
    BOOKS = "books"
    NOTES = "notes"
    DRAWING = "drawing"
    TECH = "tech"
    DORM = "dorm"
    CLOTHES = "clothes"
    OTHER = "other"


CATEGORY_LABELS = {
    Category.BOOKS: "📚 Учебники",
    Category.NOTES: "📝 Конспекты",
    Category.DRAWING: "📐 Чертёжное",
    Category.TECH: "💻 Техника",
    Category.DORM: "🏠 Для общаги",
    Category.CLOTHES: "👕 Одежда",
    Category.OTHER: "📦 Другое",
}


class CategoryCb(CallbackData, prefix="cat"):
    value: Category


class TermsCb(CallbackData, prefix="cat"):
    value: str # "free" | "exchange" | "price"


class WizardCb(CallbackData, prefix="wiz"):
    action: str  # "cancel" | "back" | "skip" | "done"