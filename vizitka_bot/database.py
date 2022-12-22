import sqlite3 as sql

db = 'vizitka_bot.db' #имя бд (ОБЯЗАТЕЛЬНО БД ДОЛЖНА ЛЕЖАТЬ В ОДНОЙ ПАПКЕ С КОДОМ)
conn = sql.connect(db, check_same_thread=False)
c = conn.cursor()

def check_step(message):
    cmd = "SELECT step FROM user WHERE user_id = '{}'".format(message.chat.id)
    c.execute(cmd)
    result = c.fetchall()[0][0]
    return result

def insert_step(n, message):
    cmd = "UPDATE user SET step = '{}' WHERE user_id = '{}'".format(n, message.chat.id)
    c.execute(cmd)
    conn.commit()