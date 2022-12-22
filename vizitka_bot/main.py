import telebot
import datetime
from database import *
from secret import TOKEN


def run():
    # Создаем экземпляр бота
    bot = telebot.TeleBot(TOKEN)

    menu_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    make_button = telebot.types.InlineKeyboardButton(text="Создать визитку")
    balance_button = telebot.types.InlineKeyboardButton(text="Баланс")
    help_button = telebot.types.InlineKeyboardButton(text="Помощь")
    menu_markup.add(make_button, balance_button, help_button)

    theme_inline_markup = telebot.types.InlineKeyboardMarkup()
    light_theme_button = telebot.types.InlineKeyboardButton(
        text="Светлая", callback_data="Светлая"
    )
    dark_theme_button = telebot.types.InlineKeyboardButton(
        text="Темная", callback_data="Темная"
    )
    theme_inline_markup.add(light_theme_button)
    theme_inline_markup.add(dark_theme_button)

    image_inline_markup = telebot.types.InlineKeyboardMarkup()
    yes_button = telebot.types.InlineKeyboardButton(
        text="Да, хочу", callback_data="Да, хочу"
    )
    no_button = telebot.types.InlineKeyboardButton(
        text="Нет, воздержусь", callback_data="Нет, воздержусь"
    )
    image_inline_markup.add(yes_button)
    image_inline_markup.add(no_button)

    @bot.message_handler(commands=["start"])
    def welcome(message):
        cmd = f"SELECT user_id FROM user WHERE id = '{message.chat.id}'"
        c.execute(cmd)
        exist = c.fetchone()
        if exist is None:
            bot.send_message(
                message.chat.id,
                "Привет! В этом боте ты сможешь сгенерировать свою визитную карточку.",
            )
            cmd = f"INSERT INTO user VALUES('{message.chat.id}', '0', '{message.from_user.username}', 'default')"
            c.execute(cmd)
            conn.commit()
        bot.send_message(message.chat.id, "Добро пожаловать!", reply_markup=menu_markup)
        insert_step(1, message)

    @bot.message_handler(content_types=["text"])
    def conversation(message):
        if check_step(message) == "1":
            if message == "Создать визитку":
                cmd = f"SELECT COUNT(*) FROM card WHERE user_id = '{message.chat.id}'"
                c.execute(amount_of_user_cards)
                amount_of_user_cards = c.fetchone()[0]
                if amount_of_user_cards > 9:
                    bot.send_message(
                        message.chat.id,
                        "Создать визитку невозможно, вы уже сделали 10.",
                        reply_markup=menu_markup,
                    )
                    insert_step(1, message)
                    return
                cmd = f"INSERT INTO card (id, user_id, card_number) VALUES('{generate_id()}', '{message.chat.id}', '{amount_of_user_cards}')"
                c.execute(cmd)
                conn.commit()
                bot.send_message(
                    message.chat.id,
                    "Выберите цветовую схему визитной карточки:",
                    reply_markup=theme_inline_markup,
                )
                insert_step(1.1, message)
            elif message == "Баланс":
                insert_step(2, message)
            elif message == "Помощь":
                insert_step(3, message)
            else:
                bot.send_message(
                    message.chat.id,
                    "Я не понимаю такую команду. Пожалуйста, выберите из предложенных.",
                    reply_markup=menu_markup,
                )
        elif check_step(message) == "1.2":
            pass
        elif check_step(message) == "1.3":
            pass
        elif check_step(message) == "1.4":
            pass
        elif check_step(message) == "1.5":
            pass
        elif check_step(message) == "2":
            pass
        elif check_step(message) == "3":
            pass
        else:
            bot.send_message(
                message.chat.id,
                "Вы не прошли регистрацию. Для регистрации напишите команду /start.",
            )

    @bot.callback_query_handler(func=lambda call: True)
    def answer(call):
        if check_step(call.message) == "1.1":
            if call.data == "Светлая":
                pass
            elif call.data == "Темная":
                pass
            else:
                bot.send_message(call.message.chat.id, "Я вас не понимаю.")

    try:
        bot.polling(none_stop=True)
    except Exception as e:
        telebot.logger.error(e)
        print("Error: " + str(datetime.datetime.now()))


if __name__ == "__main__":
    run()
