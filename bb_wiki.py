import re
import requests
import wikipedia
from bs4 import BeautifulSoup
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

import bb_info

bot = bb_info.bot

"""ОПЕРАЦИИ ДЛЯ РАБОТЫ С ВИКИПЕДИЕЙ"""

wikipedia.set_lang("ru")


# получение случайного слова из Википедии
def random_word_from_wiki():
    url = requests.get("https://ru.wikipedia.org/wiki/Special:Random")
    soup = BeautifulSoup(url.content, "html.parser")
    title = soup.find(class_="firstHeading").text
    return title


# валидация
def validating(text):
    # против заголовков
    for symbol in range(len(text)):
        if text[symbol] == '\n' and text[symbol + 1] == '=':
            text = text[:symbol - 2]
    # против скобок
    text = re.sub(r"\(.+?\)\s", '', text)
    return text


# получение определения
def get_wiki_summary(word):
    try:
        summary = wikipedia.summary(word, sentences=2)
        summary = validating(summary)
        return summary
    except:
        return None


# отправка определения
def send_wiki_summary(word):
    w = word.text
    summary = get_wiki_summary(w)
    if summary is not None:
        bot.send_message(word.chat.id, summary)
    else:
        bot.send_message(word.chat.id, "Статья не найдена")


def markup_wiki():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Случайная статья", callback_data="wiki_random"))
    return markup


@bot.callback_query_handler(func=lambda call: call.data.startswith('wiki'))
def callback_query(call):
    if call.data == "wiki_random":
        word = random_word_from_wiki()
        bot.send_message(call.message.chat.id, get_wiki_summary(word))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Википедия 🧩",
                              reply_markup=None)
