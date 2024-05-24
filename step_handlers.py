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

    # Проверяем формат
    if ' | ' in message.text:
        data = message.text.split(' | ')
        
        # Проверки на наличие необходимых прав
        try:
            member_info = bot.get_chat_member(data[0], bot.get_me().id)

            if member_info.can_invite_users == True:
                # Собираем клавиатуру и отправляем предпросмотр
                if ch_type == 'necessary': to_send = 'Обязательный'
                elif ch_type == 'closed': to_send = 'Закрытый'

                callback = f'confirm_channel:{data[0]}:{data[1]}:{ch_type}'
                bot.send_message(message.chat.id, 'Добавить канал?\n\nНазвание: ' + data[1] + '\nID: ' + data[0] + '\nТип: ' + to_send, reply_markup = keyboards.confirm_chan_action(callback, ch_type))
            else:
                bot.send_message(message.chat.id, 'Бот не является админом/у бота не права на приглашение пользователей!')
        except:
            back_button = types.InlineKeyboardButton('Назад', callback_data = ch_type)
            keyboard = types.InlineKeyboardMarkup(row_width=1).add(back_button)
            bot.send_message(message.chat.id, 'Бота нет в канале!', reply_markup = keyboard)
    else:
        bot.send_message(message.chat.id, 'Неверный формат!')

def edit_chan_name(message, chan, to_edit):
    bot.edit_message_text(chat_id = to_edit.chat.id, message_id = to_edit.message_id, text = 'Обработка...') 

    callback = f'edit_chan_name:{chan[0]}:{message.text}'
    bot.send_message(message.chat.id, f'Записать изменения в канал "{chan[1]}"?', reply_markup = keyboards.confirm_chan_action(callback, 'channels_menu'))

def ban_user(message, action, to_edit):
    bot.edit_message_text(chat_id = to_edit.chat.id, message_id = to_edit.message_id, text = 'Обработка...')
    user = db.get_user(message.text)

    if user:
        callback = f'{action}:{message.text}'
        bot.send_message(message.chat.id, f'Ты уверен,что хочешь заблокировать / разблокировать пользователя @{user[1]}?', reply_markup = keyboards.confirm_chan_action(callback, 'ban_user'))
    else:
        bot.send_message(message.chat.id, 'Пользователь не найден!')

def add_admin(message, to_edit):
    bot.edit_message_text(chat_id = to_edit.chat.id, message_id = to_edit.message_id, text = 'Обработка...')

    try:
        db.add_admin(message.text)
        bot.send_message(message.chat.id, 'Админ успешно добавлен!', reply_markup = keyboards.ready_keyboard)
    except:
        bot.send_message(message.chat.id, 'Пользователя нет в базе данных!', reply_markup = keyboards.cancel_keyboard)
