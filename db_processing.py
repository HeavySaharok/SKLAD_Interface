import sqlite3


con = sqlite3.connect("main_storage.db")
cur = con.cursor()
result = cur.execute("""SELECT * FROM basic_store
            WHERE type = 1""").fetchall()
for elem in result:
    print(elem)
con.close()
