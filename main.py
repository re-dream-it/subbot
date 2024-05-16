import time
import telebot
from telebot import types
import config
from db import DB
import buttons as keyboards

# INIT
db = DB('db.db')
bot = telebot.TeleBot(config.token)

# Обработка команды /start
@bot.message_handler(commands = ['start'])
def law(message):
    user = db.get_user(message.chat.id)

    # Проверка на наличие бана
    if(user[4]): return

    # Проверка на админа.
    if(db.check_admin(message.chat.id)):
        bot.send_message(message.chat.id, 'Привет, ' + message.chat.first_name + ', что ты хочешь сделать?', reply_markup = keyboards.admin_keyboard)
    else:
        try:
            # Добавляем пользователя в базу данных, если его там нет.
            if (not db.check_user(message.chat.id)):
                db.add_user(message.chat.id, message.chat.username, message.chat.first_name)
        except Exception as e:
            # Обрабатываем ошибку, в случае ее возникновения.
            print(e)
            bot.send_message(message.chat.id, '⚠️ Возникла ошибка при запуске бота!\n\nПожалуйста, обратитесь в тех. поддержку: @re_dream') 

        # Проверка на наличие каналов в БД.
        channels = db.get_all_channels
        if(bool(channels)):
            # Есть каналы.
            bot.send_message(message.chat.id, 'Список каналов') 
        else:
            # Нет каналов.
            bot.send_message(message.chat.id, 'Привет, ' + message.chat.first_name + ', скоро я дам о себе знать...') 

    # Обнуляем состояние.
    db.set_status(message.chat.id, '0')

@bot.message_handler(content_types = ['text'])
def law(message):
    user = db.get_user(message.chat.id)
    status = user[3]

    # Проверка на наличие бана
    if(user[4]):
        return
        

@bot.callback_query_handler(func = lambda call: True)
def callback_inline(call):
    user = db.get_user(call.message.chat.id)

    # Проверка на наличие бана
    if(user[4]): return
    
    # Админ панель

    # Открытие админ панели.
    if call.data == 'admin_panel':
        bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'Привет, ' + call.message.chat.first_name + ', что ты хочешь сделать?', reply_markup = keyboards.admin_keyboard)
        db.set_status(call.message.chat.id, '0')

    # Меню выбора фильтра по жанру.
    elif call.data == 'edit_channels':
        bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'Что будем делать?', reply_markup = keyboards.channel_edit_keyboard)
    
    elif call.data == 'add_channel':
        bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'Какие каналы необходимо добавить?', reply_markup = keyboards.channel_add_keyboard)

    elif call.data == 'necessary' or call.data == 'closed':
        msg = bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'Пришли id обязательного/закрытого канала и Название кнопки в следующем формате:\n\nID | Название кнопки', reply_markup = keyboards.cancel_keyboard)
        if call.data == 'necessary': bot.register_next_step_handler(msg, add_necessary_step)
        elif call.data == 'closed': bot.register_next_step_handler(msg, add_closed_step)


# Обработчики некст степов
def add_necessary_step(message):
    bot.send_message(message.chat.id, 'Обязательный')

def add_closed_step(message):
    bot.send_message(message.chat.id, 'Закрытый')
    
   

    # Обычные кнопки


# while True:
#     try:
#         bot.polling(non_stop = True, interval = 0)
#     except Exception as e:
#         print(e)                    
#         time.sleep(3)
#         continue

bot.polling(non_stop = True, interval = 0)
# bot.register_next_step_handler(message, vvod_rub, data) хендлер юзай