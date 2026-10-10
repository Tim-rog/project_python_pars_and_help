from sqlalchemy import create_engine, text, insert, MetaData
from data import settings
import pandas as pd


engine = create_engine(
    url=settings.DATABASE_URL,
    echo=False,
    pool_size=5,
    max_overflow=10
)


def chats(user, ch):
    print(user, ch)
    new = 0
    with engine.connect() as conn:
        if conn.execute(text(f"""SELECT COUNT(*) FROM "CHATS" WHERE chat = :ch AND user_id= :id"""), {'ch': int(ch), 'id':int(user)}).scalar() == 0:
            conn.execute(text(f'INSERT INTO "CHATS" VALUES ({int(ch)}, {int(user)});'))
            new = True
        conn.commit()
    return new


def get_chats(ch):
    with engine.connect() as conn:
        res = conn.execute(text(f"""SELECT user_id FROM "CHATS" WHERE chat = :ch"""), {'ch': int(ch)})
        return res.all()


def create_list(user, message):
    print(user)
    with engine.connect() as conn:
        res = conn.execute(text(f"SELECT COUNT(*) FROM lists WHERE user_id='{user}'"))
        r = (res.all()[0][0])
        print(r)
        r = str(r)+str(user)
        conn.execute(text(f"INSERT INTO lists VALUES ('{r}', '{message}', 0, 2, 7, '{user}');"))
        conn.commit()


def in_did(user):
    with engine.connect() as conn:
        res = conn.execute(text(f"SELECT COUNT(*) FROM lists WHERE user_id='{user}' AND task=''"))
        if res.all()[0][0] > 0:
            return True
        return False


def get_index(user, char=''):
    with engine.connect() as conn:
        res = conn.execute(text(f"SELECT t_id FROM lists WHERE user_id='{user}' AND task='{char}'"))
        r = str((res.all()[0][0]))
        return r


def pool(index, task):
    with engine.connect() as conn:
        conn.execute(text("""UPDATE lists SET task= :tx WHERE t_id= :id"""), {"tx": task, "id":index})
        conn.commit()


def unleash(user):
    with engine.connect() as conn:
        res = conn.execute(text(f"SELECT * FROM lists WHERE user_id='{user}'"))
        res2 = res.all()
        c = ['t_id', 'task', 'status', 'category', 'important', 'user_id']
        data = pd.DataFrame(columns=c)
        for i in range(0, len(res2)):
            for n in range(0, len(c)):
                data.loc[i, c[n]] = res2[i][n]
        return data


def drop(user, ind):
    with engine.connect() as conn:
        i = str(ind) + str(user)
        conn.execute(text(f"DELETE FROM lists * WHERE t_id='{i}'"))
        conn.commit()


def change_dt(user, ind):
    with engine.connect() as conn:
        i = str(ind) + str(user)
        conn.execute(text(f"UPDATE lists SET task='' WHERE t_id='{i}';"))
        conn.commit()


def status_dt(user, ind, r):
    with engine.connect() as conn:
        i = str(ind) + str(user)
        conn.execute(text(f"UPDATE lists SET status={r} WHERE t_id='{i}';"))
        conn.commit()

def sorted_list(sort_type, user):
    with engine.connect() as conn:
        res = conn.execute(
            text(f"SELECT * FROM lists WHERE user_id = '{user}'"),
        )
        res2 = res.all()

        columns = ['t_id', 'task', 'status', 'category', 'important', 'user_id']
        data = pd.DataFrame(res2, columns=columns)
        print(data)


        if sort_type == 'im':
            sorted_data = data.sort_values(by='important')
        elif sort_type == 'lt':
            sorted_data = data.sort_values(by='t_id', ascending=False)
        elif sort_type=='od':
            sorted_data = data.sort_values(by='t_id', ascending=True)
        else:
            pass
        print(sorted_data)
        return sorted_data
