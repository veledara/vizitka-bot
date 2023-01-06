import telebot
import datetime
from database import *
from draw_info_on_image import *
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
            c.execute(
                f"INSERT INTO user (id, step, tg_username) VALUES('{message.chat.id}', '0', '{message.from_user.username}')"
            )
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
                c.execute(
                    f"SELECT COUNT(*) FROM card WHERE user_id = '{message.chat.id}'"
                )
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
                c.execute(
                    f"INSERT INTO card (id, user_id, card_number) VALUES('{card_id}', '{message.chat.id}', '{amount_of_user_cards}')"
                )
                c.execute(
                    f"UPDATE user SET current_card = '{card_id}' WHERE id = '{message.chat.id}'"
                )
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
            c.execute(
                f"UPDATE card SET name = '{message.text}' WHERE id = '{current_card_check(message)}'"
            )
            conn.commit()
            bot.send_message(
                message.chat.id,
                "Отлично! Теперь введите номер телефона, который хотите видеть на карте:",
            )
            insert_step(1.3, message)
        elif check_step(message) == "1.3":
            c.execute(
                f"UPDATE card SET phone = '{message.text}' WHERE id = '{current_card_check(message)}'"
            )
            conn.commit()
            bot.send_message(
                message.chat.id,
                "Супер! Теперь введите название компании, в которой работаете:",
            )
            insert_step(1.4, message)
        elif check_step(message) == "1.4":
            c.execute(
                f"UPDATE card SET company = '{message.text}' WHERE id = '{current_card_check(message)}'"
            )
            conn.commit()
            bot.send_message(
                message.chat.id,
                "Хотите ли добавить фотографию на карточку?",
                reply_markup=choice_inline_markup,
            )
            insert_step(1.5, message)
        elif check_step(message) == "2":
            pass
        elif check_step(message) == "3":
            pass
        else:
            if check_step(message) == "1.1":
                bot.send_message(
                    message.chat.id, "Выберите из двух вариантов: темная/светлая."
                )
            elif check_step(message) == "1.6":
                bot.send_message(
                    message.chat.id,
                    "Вы должны отправить фотографию/изображение, желательно формата 3:4.",
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
        if check_step(message) == "1.6":
            image_id = message.photo[-1].file_id
            file_info = bot.get_file(image_id)
            photo = bot.download_file(file_info.file_path)
            c.execute(
                "UPDATE card SET file_id = ?, file_data = ? WHERE id = ?",
                (image_id, photo, current_card_check(message)),
            )
            conn.commit()
            bot.send_message(
                message.chat.id,
                "Супер! Карточка готова!",
            )
            generator(message)
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
            c.execute(
                f"UPDATE card SET theme = '{theme}' WHERE id = '{current_card_check(call.message)}'"
            )
            conn.commit()
            bot.send_message(
                call.message.chat.id,
                "Введите имя, которое хотите видеть на карте:",
            )
            insert_step(1.2, call.message)
        elif check_step(call.message) == "1.5":
            if call.data == "Да, хочу":
                step = 1.6
                message = "Отправьте фотографию (желательно 4 на 3)."
            else:
                step = 1
                message = "Карточка готова."
                generator(call.message)
            bot.send_message(call.message.chat.id, message)
            insert_step(step, call.message)
        else:
            bot.send_message(
                call.message.chat.id,
                "Вы уже сделали свой выбор.",
            )

    def generator(message):
        select_stmt = f"SELECT * FROM card WHERE id = '{current_card_check(message)}'"
        c.execute(select_stmt)
        cort = c.fetchall()
        file_data = cort[0][8] if cort[0][8] != None else None
        image_bytes = visit_card_maker(cort[0][1], cort[0][2], cort[0][3], cort[0][4], file_data)
        bot.send_photo(message.chat.id, image_bytes)

    # try:
    bot.polling(none_stop=True)
    # except Exception as e:
    #    telebot.logger.error(e)
    #   print("Error: " + str(datetime.datetime.now()))


if __name__ == "__main__":
    run()
