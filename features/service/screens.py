from . import texts
from .keyboards import categories_kb, nav_kb
from .states import NewItem

SCREENS = {
    NewItem.category: (texts.ASK_CATEGORY, categories_kb),
    NewItem.title.state: (texts.ASK_TITLE, lambda: nav_kb(back=True)),
}
