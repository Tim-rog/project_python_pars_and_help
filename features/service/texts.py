from aiogram import html

from .callbacks import CATEGORY_LABELS

TOTAL_STEPS = 7

def step(n: int, question: str) -> str:
    return f"📝 Новое объявление • Шаг {n}/{TOTAL_STEPS}\n\n{question}"


def published(title: str) -> str:
    return PUBLISHED.format(title=html.quote(title))


def item_preview(data: dict) -> str:
    terms = TERMS_LABELS[data["terms"]]

    if data["terms"] == "exchange":
        terms += f": {html.quote(data['exchange'])}"
    elif data["terms"] == "price":
        terms += f": {html.quote(str(data['price']))} ₽"

    title = html.quote(data["title"])
    description = html.quote(data["description"])
    place = html.quote(data["place"])

    category = html.quote(
        data.get("category", "Не указана")
    )

    return (
        "🔍 <b>Проверь объявление</b>\n"
        "<i>Вот так его увидят другие студенты</i>\n\n"
        f"📦 <b>{title}</b>\n"
        f"{CATEGORY_LABELS[category]}\n\n"
        "📋 <b>Описание:</b>\n"
        f"{description}\n\n"
        f"<b>{terms}</b>\n"
        f"📍 <b>Место:</b> {place}\n"
        "───────────────────\n"
        "Всё верно? Опубликуй объявление "
        "или вернись к редактированию."
    )

ACTION_CANCELED = "❌ Создание отменено."
TEXT_NEEDED = "На этом шаге нужно отправить <b>текст</b>."
INVALID_PRICE = "Укажи цену числом, например <b>500</b>."
PHOTO_NEEDED = "На этом шаге нужно отправить <b>фото</b>."
ASK_CATEGORY = "<b>Что отдаёшь?</b>\n\nВыбери категорию вещи."
ASK_TITLE = "<b>Как назовём вещь?</b>\n\nНапиши короткое и понятное название."
ASK_DESCRIPTION = "<b>Добавим описание</b>.\n\nРасскажи о состоянии и особенностях вещи."
ASK_PHOTOS = "<b>Есть фото?</b>\n\nПришли фотографию вещи или пропусти этот шаг."
ASK_TERMS = "<b>На каких условиях?</b>\n\nОтдашь бесплатно, обменяешь на что-то или продашь?"
ASK_TRADE = "<b>Что хочешь взамен?</b>\n\nНапиши, что тебе было бы интересно получить в обмен."
ASK_PRICE = "<b>Сколько просишь?</b>\n\n Укажи цену в рублях, одним числом."
ASK_PLACE = "<b>Где можно забрать?</b>\n\nВыбери корпус или общежитие из списка либо напиши свой вариант."
PUBLISHED = (
    "✅ <b>Объявление опубликовано!</b>\n\n"
    "«<b>{title}</b>» теперь в барахолке. Когда кто-то заинтересуется, "
    "я пришлю тебе сообщение со ссылкой на его профиль.\n\n"
    "Объявление можно найти в «<b>Мои объявления</b>» и закрыть, "
    "когда вещь найдёт нового хозяина."
)

TERMS_LABELS = {
    "free": "🎁 Бесплатно",
    "exchange": "🔄 Обмен",
    "price": "💰 Цена",
}

CANCELLED = "Создание объявления отменено."