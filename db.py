import sqlite3

conn = sqlite3.connect("database.db",check_same_thread=False)
conn.row_factory = sqlite3.Row


def init_database():
    cursor = conn.cursor()
    cursor.execute("create table if not exists tasks (id integer primary key Autoincrement,"
                   "title text not null,"
                   "done integer default 0)")
    conn.commit()
    print("Database initialized")


