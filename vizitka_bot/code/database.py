import sqlite3 as sql
import uuid

db = r"vizitka_bot\databases\vizitka_bot.db"  # имя бд (ОБЯЗАТЕЛЬНО БД ДОЛЖНА ЛЕЖАТЬ В ОДНОЙ ПАПКЕ С КОДОМ)
conn = sql.connect(db, check_same_thread=False)
c = conn.cursor()


def generate_id():
    return str(uuid.uuid4())


def check_step(message):
    c.execute(f"SELECT step FROM user WHERE id = '{message.chat.id}'")
    result = c.fetchall()[0][0]
    return result


def insert_step(n, message):
    c.execute(f"UPDATE user SET step = '{n}' WHERE id = '{message.chat.id}'")
    conn.commit()


def user_exist(message):
    c.execute(f"SELECT id FROM user WHERE id = '{message.chat.id}'")
    exist = c.fetchone()
    return False if exist == None else True
    

def current_card_check(message):
    c.execute(f"SELECT current_card FROM user WHERE id = '{message.chat.id}'")
    result = c.fetchall()[0][0]
    return result


def clear_table(database_path: str, table_name: str):
    conn = sql.connect(database_path)
    c = conn.cursor()
    c.execute(f"DELETE FROM {table_name};")
    conn.commit()
    conn.close()


if __name__ == "__main__":
    clear_table(r"vizitka_bot\databases\vizitka_bot.db", "card")
    clear_table(r"vizitka_bot\databases\vizitka_bot.db", "user")
