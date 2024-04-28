import sqlite3


def create_table(name):
    """
    Создаёт таблицу склада в БД
    """
    con = sqlite3.connect("main_database.db")
    cur = con.cursor()
    cur.execute(f"""CREATE TABLE {name} (
        id INTEGER NOT NULL UNIQUE,
        amount INTEGER NOT NULL,
        PRIMARY KEY (id))""").fetchall()
    con.commit()
    con.close()


def delete_table(name):
    """
    Удаляет таблицу склада в БД
    """
    con = sqlite3.connect("main_database.db")
    cur = con.cursor()
    cur.execute(f"""DROP TABLE {name}""")
    con.commit()
    con.close()


def table_data(name):
    """
    Выводит содержимое таблицы из неё
    """
    con = sqlite3.connect("main_database.db")
    cur = con.cursor()
    cur.execute(f"""SELECT * from {name}""")
    return cur.fetchall()
