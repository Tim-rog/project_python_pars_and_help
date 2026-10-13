from . import texts
from .keyboards import categories_kb, nav_kb, terms_kb
from .states import NewItem

SCREENS = {
    NewItem.category: (texts.ASK_CATEGORY, categories_kb),
    NewItem.title.state: (texts.ASK_TITLE, lambda: nav_kb(back=True)),
    NewItem.description.state: (texts.ASK_DESCRIPTION, lambda: nav_kb(back=True)),
    NewItem.photos.state: (texts.ASK_PHOTOS, lambda: nav_kb(back=True, skip=True)),
    NewItem.terms.state: (texts.ASK_TERMS, terms_kb),
    # NewItem.terms_trade.state: (texts.ASK_TRADE, lambda: nav_kb(back=True)),
    # NewItem.terms_price.state: (texts.ASK_PRICE, lambda: nav_kb(back=True)),
    NewItem.place.state: (texts.ASK_PLACE, lambda: nav_kb(back=True)),
    NewItem.preview.state: ("заглушка", lambda: nav_kb(back=True)),
}
