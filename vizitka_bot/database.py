import sqlite3 as sql
import uuid

db = 'vizitka_bot.db' #имя бд (ОБЯЗАТЕЛЬНО БД ДОЛЖНА ЛЕЖАТЬ В ОДНОЙ ПАПКЕ С КОДОМ)
conn = sql.connect(db, check_same_thread=False)
c = conn.cursor()

def generate_id():
    return str(uuid.uuid4())

def check_step(message):
    cmd = "SELECT step FROM user WHERE id = '{}'".format(message.chat.id)
    c.execute(cmd)
    result = c.fetchall()[0][0]
    return result

def insert_step(n, message):
    cmd = "UPDATE user SET step = '{}' WHERE id = '{}'".format(n, message.chat.id)
    c.execute(cmd)
    conn.commit()