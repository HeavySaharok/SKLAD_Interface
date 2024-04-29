import sqlite3


def create_table(name):
    """
    Создаёт таблицу склада в БД
    """
    con = sqlite3.connect("db/main_database.db")
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
    con = sqlite3.connect("db/main_database.db")
    cur = con.cursor()
    cur.execute(f"""DROP TABLE {name}""")
    con.commit()
    con.close()


def table_data(name):
    """
    Выводит содержимое таблицы из неё
    """
    con = sqlite3.connect("db/main_database.db")
    cur = con.cursor()
    cur.execute(f"""SELECT * from {name}""")
    return cur.fetchall()


def table_edit(name, id, amount, oper='input'):
    """
    Редактирует выбранный предмет из выбранной таблицы
    """
    con = sqlite3.connect("db/main_database.db")
    cur = con.cursor()
    if oper == 'output':
        if name != 'outside':
            cur.execute(f"""UPDATE {name} set amount = amount - {amount} where id = {id}""")
            con.commit()
            cur.execute(f"""DELETE from {name} where amount = 0""")
            con.commit()
            con.close()
    if oper == 'input':
        flag = cur.execute(f"""SELECT * from {name} where id = {id}""").fetchall()
        if flag:
            if name != 'outside':
                cur.execute(f"""UPDATE {name} set amount = amount + {amount} where id = {id}""")
                con.commit()
                con.close()
        else:
            if name != 'outside':
                cur.execute(f"""INSERT into {name} (id, amount) VALUES ({id}, {amount})""")
                con.commit()
                con.close()
