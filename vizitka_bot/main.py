import telebot
import datetime
from database import *
from secret import TOKEN


def run():
    # Создаем экземпляр бота
    bot = telebot.TeleBot(TOKEN)

    menu_markup = telebot.types.ReplyKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=True
    )
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

    choice_inline_markup = telebot.types.InlineKeyboardMarkup()
    yes_button = telebot.types.InlineKeyboardButton(
        text="Да, хочу", callback_data="Да, хочу"
    )
    no_button = telebot.types.InlineKeyboardButton(
        text="Нет, воздержусь", callback_data="Нет, воздержусь"
    )
    choice_inline_markup.add(yes_button)
    choice_inline_markup.add(no_button)

    @bot.message_handler(commands=["start"])
    def welcome(message):
        if not user_exist(message):
            bot.send_message(
                message.chat.id,
                "Привет! В этом боте ты сможешь сгенерировать свою визитную карточку.",
            )
            cmd = f"INSERT INTO user (id, step, tg_username) VALUES('{message.chat.id}', '0', '{message.from_user.username}')"
            c.execute(cmd)
            conn.commit()
        bot.send_message(message.chat.id, "Добро пожаловать!", reply_markup=menu_markup)
        insert_step(1, message)

    @bot.message_handler(content_types=["text"])
    def conversation(message):
        if not user_exist(message):
            bot.send_message(
                message.chat.id,
                "Вы не прошли регистрацию. Для регистрации напишите команду /start.",
            )
            return
        if check_step(message) == "1":
            if message.text == "Создать визитку":
                cmd = f"SELECT COUNT(*) FROM card WHERE user_id = '{message.chat.id}'"
                c.execute(cmd)
                amount_of_user_cards = c.fetchone()[0]
                if amount_of_user_cards > 9:
                    bot.send_message(
                        message.chat.id,
                        "Создать визитку невозможно, вы уже сделали 10.",
                        reply_markup=menu_markup,
                    )
                    insert_step(1, message)
                    return
                card_id = generate_id()
                cmd = f"INSERT INTO card (id, user_id, card_number) VALUES('{card_id}', '{message.chat.id}', '{amount_of_user_cards}')"
                c.execute(cmd)
                cmd = f"UPDATE user SET current_card = '{card_id}' WHERE id = '{message.chat.id}'"
                c.execute(cmd)
                conn.commit()
                bot.send_message(
                    message.chat.id,
                    "Выберите цветовую схему визитной карточки:",
                    reply_markup=theme_inline_markup,
                )
                insert_step(1.1, message)
            elif message.text == "Баланс":
                insert_step(2, message)
            elif message.text == "Помощь":
                insert_step(3, message)
            else:
                bot.send_message(
                    message.chat.id,
                    "Я не понимаю такую команду. Пожалуйста, выберите из предложенных.",
                    reply_markup=menu_markup,
                )
        elif check_step(message) == "1.2":
            name_on_card = message.text
            cmd = f"UPDATE card SET name = '{name_on_card}' WHERE id = '{current_card_check(message)}'"
            c.execute(cmd)
            conn.commit()
            bot.send_message(
                message.chat.id,
                "Отлично! Теперь введите номер телефона, который хотите видеть на карте:",
            )
            insert_step(1.3, message)
        elif check_step(message) == "1.3":
            phone_on_card = message.text
            cmd = f"UPDATE card SET phone = '{phone_on_card}' WHERE id = '{current_card_check(message)}'"
            c.execute(cmd)
            conn.commit()
            bot.send_message(
                message.chat.id,
                "Супер! Теперь введите название компании, в которой работаете:",
            )
            insert_step(1.4, message)
        elif check_step(message) == "1.4":
            company_on_card = message.text
            cmd = f"UPDATE card SET company = '{company_on_card}' WHERE id = '{current_card_check(message)}'"
            c.execute(cmd)
            conn.commit()
            bot.send_message(
                message.chat.id,
                "Хотите ли добавить фотографию на карточку?",
                reply_markup=choice_inline_markup,
            )
            insert_step(1.5, message)
        elif check_step(message) == "1.6":
            bot.send_message(
                message.chat.id, "Отправьте фотографию (желательно 4 на 3)."
            )

        elif check_step(message) == "1.7":
            bot.send_message(message.chat.id, "Карточка готова.")
        elif check_step(message) == "2":
            pass
        elif check_step(message) == "3":
            pass
        else:
            if check_step(message) == "1.1":
                bot.send_message(
                    message.chat.id, "Выберите из двух вариантов: темная/светлая."
                )
            else:
                bot.send_message(message.chat.id, "Произошла необработнная ошибка.")

    @bot.message_handler(content_types=["photo"])
    def save_photo(message):
        if not user_exist(message):
            bot.send_message(
                message.chat.id,
                "Вы не прошли регистрацию. Для регистрации напишите команду /start.",
            )
            return
        if check_step(message) == 1.6:
            file_id = message.photo[-1].file_id
            file_info = bot.get_file(file_id)
            photo = bot.download_file(file_info.file_path)
            c.execute(
                f"UPDATE card SET file_id = '{file_id}', file_data = '{photo}' WHERE id = '{current_card_check(message)}'"
            )
            conn.commit()
            conn.close()
        else:
            bot.send_message(message.chat.id, "Зачем мне это изображение?")

    @bot.callback_query_handler(func=lambda call: True)
    def answer(call):
        if not user_exist(call.message):
            bot.send_message(
                call.message.chat.id,
                "Вы не прошли регистрацию. Для регистрации напишите команду /start.",
            )
            return
        if check_step(call.message) == "1.1":
            theme = "light" if call.data == "Светлая" else "dark"
            cmd = f"UPDATE card SET theme = '{theme}' WHERE id = '{current_card_check(call.message)}'"
            c.execute(cmd)
            conn.commit()
            bot.send_message(
                call.message.chat.id,
                "Введите имя, которое хотите видеть на карте:",
            )
            insert_step(1.2, call.message)
        elif check_step(call.message) == "1.5":
            step = "1.6" if call.data == "Да, хочу" else "1.7"
            insert_step(step, call.message)
        else:
            bot.send_message(
                call.message.chat.id,
                "Произошла неизвестная ошибка.",
            )

    try:
        bot.polling(none_stop=True)
    except Exception as e:
        telebot.logger.error(e)
        print("Error: " + str(datetime.datetime.now()))


if __name__ == "__main__":
    run()
