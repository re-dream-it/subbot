import time
import telebot
from telebot import types
import config
from db import DB
import buttons as keyboards
import step_handlers

# INIT
db = DB('db.db')
bot = telebot.TeleBot(config.token)

# Обработка команды /start
@bot.message_handler(commands = ['start'])
def law(message):
    bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
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
    # мейби убирать

@bot.message_handler(content_types = ['text'])
def law(message):
    user = db.get_user(message.chat.id)
    status = user[3]

    if message.text == 'testit':
        while True:
            bot.send_message(message.chat.id, 'Список каналов')
        
    if message.text == 'answer':
        
        bot.send_message(message.chat.id, 'ААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААААА')
    

    # Проверка на наличие бана
    if(user[4]): return
        

@bot.callback_query_handler(func = lambda call: True)
def callback_inline(call):
    user = db.get_user(call.message.chat.id)
    bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)

    # Проверка на наличие бана
    if(user[4]): return
    
    # Админ панель

    # Открытие админ панели.
    if call.data == 'admin_panel':
        bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'Привет, ' + call.message.chat.first_name + ', что ты хочешь сделать?', reply_markup = keyboards.admin_keyboard)
        db.set_status(call.message.chat.id, '0')

    # Меню редактирования каналов.
    elif call.data == 'channels_menu':
        bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'Что будем делать?', reply_markup = keyboards.channel_edit_keyboard)
    
    # Выбирают добавить канал.
    elif call.data == 'add_channel':
        bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'Какие каналы необходимо добавить?', reply_markup = keyboards.channel_add_keyboard)

    # Выбирают тип канала.
    elif call.data == 'necessary' or call.data == 'closed':
        msg = bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'Пришли id обязательного/закрытого канала и Название кнопки в следующем формате:\n\nID | Название кнопки', reply_markup = keyboards.cancel_keyboard)
        bot.register_next_step_handler(msg, step_handlers.add_chan_step, call.data, msg)

    # Подтвердили добавление канала
    elif 'confirm_channel:' in call.data:
        data = call.data.split(':')

        if data[3] == 'necessary':
            link = bot.create_chat_invite_link(data[1], 'Пригласительная ссылка кнопки').invite_link 
        else:
            link = '0'

        db.add_chan(data[1], data[2], data[3], link)
        bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'Канал успешно добавлен!')

    # Редактировать / удалить каналы
    elif 'edit_channels:' in call.data:
        action = call.data.split(':')[1]
        channels = db.get_all_channels()

        bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'Какой канал нужно удалить / редактировать?', reply_markup = keyboards.form_edit_chans(action, channels))

    # Действие с каналом
    elif 'channel_action:' in call.data:
        print(1)
        data = call.data.split(':')
        chan = db.get_chan(data[1])
        print(data[1])
        print(chan)

        if data[2] == 'delete':
            callback = f'delete_channel:{data[1]}'
            bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = f'Ты уверен что хочешь удалить канал "{chan[1]}"?', reply_markup = keyboards.confirm_chan_action(callback, 'admin_panel'))
        elif data[2] == 'edit':
            msg = bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'Пришли новое название кнопки', reply_markup = keyboards.cancel_keyboard)
            bot.register_next_step_handler(msg, step_handlers.edit_chan_name, chan, msg)

    # Подтвердить удаление
    elif 'delete_channel:' in call.data:
        chan_id = call.data.split(':')[1]
        chan = db.get_chan(chan_id)
        db.delete_chan(chan_id)

        bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = f'Отлично, канал "{chan[1]}" удален', reply_markup = keyboards.ready_keyboard)

    # Подтвердить изменение названия
    elif 'edit_chan_name:' in call.data:
        chan_id = call.data.split(':')[1]
        new_name = call.data.split(':')[2]

        db.set_chan_name(chan_id, new_name)
        bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'Изменения записаны!')

    elif call.data == 'ban_users':
        bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'Что будем делать?', reply_markup = keyboards.ban_menu_keyboard)

    elif call.data == 'ban_user' or call.data == 'unban_user':
        msg = bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'Отправь id пользователя', reply_markup = keyboards.cancel_keyboard)
        bot.register_next_step_handler(msg, step_handlers.ban_user, call.data, msg)
    
    elif 'ban_user:' in call.data or 'unban_user:' in call.data:
        data = call.data.split(':')

        if 'ban_user:' in call.data: db.set_ban(data[1], 1)
        elif 'ban_user:' in call.data: db.set_ban(data[1], 0)

        bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'Действие выполнено!')


    elif call.data == 'edit_admin':
        bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'Что ты хочешь сделать?', reply_markup = keyboards.admin_edit_keyboard)

    elif call.data == 'delete_admin':
        admins = db.get_admins()

        bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'Кого нужно удалить?', reply_markup = keyboards.form_admins_list('delete', admins))

    if 'admin_action:' in call.data:
        data = call.data.split(':')

        if data[2] == 'delete':
            db.delete_admin(data[1])
            bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = f'Админ {data[1]} ражалован!', reply_markup = keyboards.ready_keyboard)

    elif call.data == 'add_admin':
        msg = bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'Отправь id пользователя', reply_markup = keyboards.cancel_keyboard)
        bot.register_next_step_handler(msg, step_handlers.add_admin, msg)
    
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