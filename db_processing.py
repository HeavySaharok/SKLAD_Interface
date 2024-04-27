# Импорт библиотеки
import sqlite3


def create_table(name):
    # Подключение к БД
    con = sqlite3.connect("db/main_storage.db")

    # Создание курсора
    cur = con.cursor()

    # Выполнение запроса и получение всех результатов
    cur.execute(f"""CREATE TABLE {name} (
    id TEXT NOT NULL UNIQUE,
    amount INTEGER NOT NULL,
    PRIMARY KEY (id))""")

    con.commit()
    con.close()


create_table('WARE_C')
