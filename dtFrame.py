from sqlalchemy import create_engine, text, insert, MetaData
from data import settings
import pandas as pd


engine = create_engine(
    url=settings.DATABASE_URL,
    echo=False,
    pool_size=5,
    max_overflow=10
)


def in_chats(user, ch):
    '''Смотрит, есть ли связка чат+пользователь в базеc(chat, user_id)'''
    with engine.connect() as conn:
        new = conn.execute(text("""SELECT COUNT(*) FROM "CHATS" WHERE chat= :ch AND user_id= :id"""),
                        {'ch': int(ch), 'id': int(user)}).scalar() > 0
        conn.commit()
    return new


def add_chat(user, ch):
    '''Добавляет в базу чат+пользователь'''
    with engine.connect() as conn:
        conn.execute(text('INSERT INTO "CHATS" (chat, user_id) VALUES (:ch, :id)'),
                         {'ch': int(ch), 'id': int(user)})
        conn.commit()


def del_chat(user, ch):
    '''Удаляет из базы чат+пользователь'''
    with engine.connect() as conn:
        conn.execute(text('DELETE FROM "CHATS" WHERE chat = :ch AND user_id = :id'),
                         {'ch': int(ch), 'id': int(user)})
        conn.commit()


def get_chats(ch):
    '''Возвращает всех пользователей, связанных с данным чатом(chat -> [user_id1, user_id2,..., user_id_x])'''
    with engine.connect() as conn:
        res = conn.execute(text(f"""SELECT user_id FROM "CHATS" WHERE chat = :ch"""), {'ch': int(ch)})
        return res.all()
