import sqlite3


def create_table(name):
    """
    Создаёт таблицу склада в БД
    """
    con = sqlite3.connect("db/main_database.db")
    cur = con.cursor()
    cur.execute(f"""CREATE TABLE {name} (
        id TEXT NOT NULL UNIQUE,
        amount INTEGER NOT NULL,
        PRIMARY KEY (id))""").fetchall()
    con.commit()
    con.close()
