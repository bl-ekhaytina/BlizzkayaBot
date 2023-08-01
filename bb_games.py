import time

import telebot
from telebot.types import InlineKeyboardMarkup

import bb_info
import machine_values

bot = bb_info.bot


def markup_games():
    markup = InlineKeyboardMarkup()
    btn1 = telebot.types.InlineKeyboardButton("🎲", callback_data="games_dice")
    btn2 = telebot.types.InlineKeyboardButton("⚽", callback_data="games_football")
    btn3 = telebot.types.InlineKeyboardButton("🏀", callback_data="games_basketball")
    btn4 = telebot.types.InlineKeyboardButton("🎯", callback_data="games_darts")
    btn5 = telebot.types.InlineKeyboardButton("🎳", callback_data="games_bowling")
    btn6 = telebot.types.InlineKeyboardButton("🎰", callback_data="games_machine")
    markup.row(btn1, btn2, btn3)
    markup.row(btn4, btn5, btn6)
    return markup


@bot.callback_query_handler(func=lambda call: call.data.startswith('games'))
def callback_query(call):
    if call.data == "games_dice":
        dice_num = bot.send_dice(call.message.chat.id, emoji='🎲')
        time.sleep(5)
        bot.send_message(call.message.chat.id, f"Поздравляю, тебе выпало {dice_num.dice.value}!")
    elif call.data == "games_football":
        dice_num = bot.send_dice(call.message.chat.id, emoji='⚽')
        time.sleep(5)
        if dice_num.dice.value > 3:
            bot.send_message(call.message.chat.id, "ГОООЛ!")
        else:
            bot.send_message(call.message.chat.id, "Мимо")
    elif call.data == "games_basketball":
        dice_num = bot.send_dice(call.message.chat.id, emoji='🏀')
        time.sleep(5)
        if dice_num.dice.value > 3:
            bot.send_message(call.message.chat.id, "Молодец, ты попал в кольцо!")
        else:
            bot.send_message(call.message.chat.id, "Мимо")
    elif call.data == "games_darts":
        dice_num = bot.send_dice(call.message.chat.id, emoji='🎯')
        time.sleep(5)
        if dice_num.dice.value == 6:
            bot.send_message(call.message.chat.id, "В яблочко!")
        elif dice_num.dice.value == 1:
            bot.send_message(call.message.chat.id, "Мимо")
        else:
            bot.send_message(call.message.chat.id, "Почти попал!")
    elif call.data == "games_bowling":
        dice_num = bot.send_dice(call.message.chat.id, emoji='🎳')
        time.sleep(5)
        if dice_num.dice.value == 6:
            bot.send_message(call.message.chat.id, "Молодец, ты сбил все кегли!")
        elif dice_num.dice.value == 1:
            bot.send_message(call.message.chat.id, "Мимо")
        else:
            bot.send_message(call.message.chat.id, f"Остались кегли в кол-ве {abs(6-dice_num.dice.value)} штук")
    elif call.data == "games_machine":
        dice_num = bot.send_dice(call.message.chat.id, emoji='🎰')
        time.sleep(5)
        res = ''
        for i in range(3):
            res += machine_values.slot_machine_meaning[machine_values.slot_machine_value[dice_num.dice.value][i]]
        bot.send_message(call.message.chat.id, f"Поздравляю, тебе выпала {dice_num.dice.value} комбинация: {res}")
