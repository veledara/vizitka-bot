import telebot
import datetime
from database import *


def run():
    # Создаем экземпляр бота
    bot = telebot.TeleBot("5709805908:AAF2SliUczwMMu_eeEevm6X2ONfUpOHnbg4")

    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    make_button = telebot.types.InlineKeyboardButton(text="Создать визитку")
    balance_button = telebot.types.InlineKeyboardButton(text="Баланс")
    help_button = telebot.types.InlineKeyboardButton(text="Помощь")
    markup.add(make_button, balance_button, help_button)

    @bot.message_handler(commands=["start"])
    def welcome(message):
        cmd = "SELECT user_id FROM user WHERE user_id = '{}'".format(message.chat.id)
        c.execute(cmd)
        exist = c.fetchone()
        if exist is None:
            bot.send_message(
                message.chat.id,
                "Привет! В этом боте ты сможешь сгенерировать свою визитную карточку.",
            )
            cmd = "INSERT INTO user VALUES('{}', '0', '{}', 'default')".format(
                message.chat.id, message.from_user.username
            )
            c.execute(cmd)
            conn.commit()
        bot.send_message(message.chat.id, "Добро пожаловать!", reply_markup=markup)
        insert_step(1, message)

    @bot.message_handler(content_types=["text"])
    def conversation(message):
        if check_step(message) == "1":
            if message == "Создать визитку":
                pass
            elif message == "Баланс":
                pass
            elif message == "Помощь":
                pass
            else:
                bot.send_message(
                message.chat.id,
                "Я не понимаю такую команду. Пожалуйста, выберите из предложенных.",
                reply_markup=markup
            )
        else:
            bot.send_message(
                message.chat.id,
                "Вы не прошли регистрацию. Для регистрации напишите команду /start.",
            )

    try:
        bot.polling(none_stop=True)
    except Exception as e:
        telebot.logger.error(e)
        print("Error: " + str(datetime.datetime.now()))


if __name__ == "__main__":
    run()
