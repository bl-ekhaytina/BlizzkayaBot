import telebot
from telebot import types

import bb_games
import bb_habr
import bb_info
import bb_wiki

bot = bb_info.bot


@bot.message_handler(commands=["start"])
def hello(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Игры 🧸")
    item2 = types.KeyboardButton("Пост 😈")
    item3 = types.KeyboardButton("Википедия 🧩")
    item4 = types.KeyboardButton("Последняя статья на хабре")
    markup.add(item1, item2, item3, item4)

    bot.send_message(message.chat.id,
                     "Здравствуйте, {0.first_name}.\nЯ - <b>{1.first_name}</b>.".format(message.from_user,
                                                                                        bot.get_me()),
                     parse_mode="html", reply_markup=markup)
    sti = open('stickers/sticker.webp', 'rb')
    bot.send_sticker(message.chat.id, sti)


# запостить сообщение в канал
def post_message(message):
    try:
        bot.send_message(bb_info.id_channel, message.text)
    except telebot.apihelper.ApiTelegramException:
        bot.send_message(message.chat.id, "Опубликовать можно только текстовое сообщение")


# обработка нажатий кнопок
@bot.message_handler(content_types=["text"])
def buttons(message):
    if message.text == "Игры 🧸":
        bot.send_message(message.chat.id, "Выберите игру", reply_markup=bb_games.markup_games())
    elif message.text == "Пост 😈":
        send = bot.send_message(message.chat.id, "Введите сообщение (только текст)")
        bot.register_next_step_handler(send, post_message)
    elif message.text == "Википедия 🧩":
        send = bot.send_message(message.chat.id, "Введите слово для поиска или выберите случайную статью",
                                reply_markup=bb_wiki.markup_wiki())
        bot.register_next_step_handler(send, bb_wiki.send_wiki_summary(send))
    elif message.text == "Последняя статья на хабре":
        back_post_id = 0
        post_text = bb_habr.parser(back_post_id)
        if post_text[0] != None:
            bot.send_message(message.chat.id, post_text)
    else:
        bot.send_message(message.chat.id, "Неизвестный запрос")


bot.polling(none_stop=True)
