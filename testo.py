# Импорт библиотеки
import sqlite3


def create_table(name):
    # Подключение к БД
    con = sqlite3.connect("db/main_storage.db")

    # Создание курсора
    cur = con.cursor()

    # Выполнение запроса и получение всех результатов
    result = cur.execute(f"""CREATE TABLE "{name}" (
        "id"	TEXT NOT NULL,
        "name"	TEXT NOT NULL,
        "category"	INTEGER NOT NULL,
        "amount"	INTEGER NOT NULL,
        "price"	INTEGER NOT NULL,
        "weight"	INTEGER NOT NULL,
        "ware_id"	TEXT NOT NULL,
        PRIMARY KEY("id")
    )""")

    con.commit()
    con.close()


create_table('BIBA')