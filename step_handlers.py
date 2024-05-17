import time
import telebot
from telebot import types
import config
from db import DB
import buttons as keyboards

db = DB('db.db')
bot = telebot.TeleBot(config.token)

def add_chan_step(message, ch_type, to_edit):
    bot.edit_message_text(chat_id = to_edit.chat.id, message_id = to_edit.message_id, text = 'Обработка...') 

    if ' | ' in message.text:
        data = message.text.split(' | ')

        bot.get_chat_member(data[0], bot.get_me.id)
        

        if ch_type == 'necessary': to_send = 'Обязательный'
        elif ch_type == 'closed': to_send = 'Закрытый'

        callback = f'confirm_channel:{data[0]}:{data[1]}:{ch_type}'

        bot.send_message(message.chat.id, 'Добавить канал?\n\nНазвание: ' + data[1] + '\nID: ' + data[0] + '\nТип: ' + to_send, reply_markup = keyboards.form_add_chan_confirm(callback, ch_type))
    else:
        bot.send_message(message.chat.id, 'Неверный формат!')
    