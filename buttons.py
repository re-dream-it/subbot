import telebot
from telebot import types

# Файл для хранения статичных кнопок и клавиатур.   

# Админ клавиатура
b1 = types.InlineKeyboardButton('Назначить/удалить администратора', callback_data = 'edit_admin')
b2 = types.InlineKeyboardButton('Сделать рассылку', callback_data = 'spam')
b3 = types.InlineKeyboardButton('Проверить подписки', callback_data = 'check_subcribes')
b4 = types.InlineKeyboardButton('Получить сводку', callback_data = 'get_info')
b5 = types.InlineKeyboardButton('Редактировать каналы', callback_data = 'channels_menu')
b6 = types.InlineKeyboardButton('Блокировать / разблокировать пользователей', callback_data = 'ban_users')

admin_keyboard = types.InlineKeyboardMarkup(row_width=1).add(b1, b2, b3, b4, b5, b6)

# Меню банов
b1 = types.InlineKeyboardButton('Блокировать', callback_data = 'ban_user')
b2 = types.InlineKeyboardButton('Разблокировать', callback_data = 'unban_user')
b3 = types.InlineKeyboardButton('Отмена', callback_data = 'admin_panel')

ban_menu_keyboard = types.InlineKeyboardMarkup(row_width=2).add(b1, b2, b3)

# Меню ред. админов
b1 = types.InlineKeyboardButton('Назначить', callback_data = 'add_admin')
b2 = types.InlineKeyboardButton('Удалить', callback_data = 'delete_admin')
b3 = types.InlineKeyboardButton('Отмена', callback_data = 'admin_panel')

admin_edit_keyboard = types.InlineKeyboardMarkup(row_width=2).add(b1, b2, b3)

# Меню управления каналами
b1 = types.InlineKeyboardButton('Добавлять', callback_data = 'add_channel')
b2 = types.InlineKeyboardButton('Удалять', callback_data = 'edit_channels:delete')
b3 = types.InlineKeyboardButton('Редактировать', callback_data = 'edit_channels:edit')
b4 = types.InlineKeyboardButton('Отмена', callback_data = 'admin_panel')

channel_edit_keyboard = types.InlineKeyboardMarkup(row_width=3).add(b1, b2, b3, b4)

# Добавлять канал
b1 = types.InlineKeyboardButton('Обязательные', callback_data = 'necessary')
b2 = types.InlineKeyboardButton('Закрытые', callback_data = 'closed')
b3 = types.InlineKeyboardButton('Назад', callback_data = 'edit_channels')
b4 = types.InlineKeyboardButton('Отмена', callback_data = 'admin_panel')

channel_add_keyboard = types.InlineKeyboardMarkup(row_width=2).add(b1, b2, b3, b4)

# Отмена
b1 = types.InlineKeyboardButton('Отмена', callback_data = 'admin_panel')
cancel_keyboard = types.InlineKeyboardMarkup(row_width=2).add(b1)

# Готово
b1 = types.InlineKeyboardButton('Готово', callback_data = 'admin_panel')
ready_keyboard = types.InlineKeyboardMarkup(row_width=2).add(b1)

# Подтверждение действия с каналом
def confirm_chan_action(callback, ch_type):
    b1 = types.InlineKeyboardButton('Подтвердить', callback_data = callback)
    b2 = types.InlineKeyboardButton('Отмена', callback_data = ch_type)
    return types.InlineKeyboardMarkup(row_width=1).add(b1, b2)

# Изменение каналов
def form_edit_chans(action, channels):
    keyboard = types.InlineKeyboardMarkup(row_width=1)

    for channel in channels:
        button = types.InlineKeyboardButton(channel[1], callback_data = f'channel_action:{channel[0]}:{action}')
        keyboard.add(button)
        
    button = types.InlineKeyboardButton('Отмена', callback_data = 'admin_panel')
    keyboard.add(button)
    return keyboard

# Список админов
def form_admins_list(action, admins):
    keyboard = types.InlineKeyboardMarkup(row_width=1)

    for admin in admins:
        button = types.InlineKeyboardButton(admin[0], callback_data = f'admin_action:{admin[0]}:{action}')
        keyboard.add(button)
        
    button = types.InlineKeyboardButton('Отмена', callback_data = 'admin_panel')
    keyboard.add(button)
    return keyboard

    
