import telebot
from telebot import types

# Файл для хранения статичных кнопок и клавиатур.   

# Админ клавиатура
b1 = types.InlineKeyboardButton('Назначить/удалить администратора', callback_data = 'edit_admin')
b2 = types.InlineKeyboardButton('Сделать рассылку', callback_data = 'spam')
b3 = types.InlineKeyboardButton('Проверить подписки', callback_data = 'check_subcribes')
b4 = types.InlineKeyboardButton('Получить сводку', callback_data = 'get_info')
b5 = types.InlineKeyboardButton('Редактировать каналы', callback_data = 'edit_channels')
b6 = types.InlineKeyboardButton('Блокировать / разблокировать пользователей', callback_data = 'ban_users')

admin_keyboard = types.InlineKeyboardMarkup(row_width=1).add(b1, b2, b3, b4, b5, b6)

# Меню редактирования каналов
b1 = types.InlineKeyboardButton('Добавлять', callback_data = 'add_channel')
b2 = types.InlineKeyboardButton('Удалять', callback_data = 'delete_channel')
b3 = types.InlineKeyboardButton('Редактировать', callback_data = 'edit_channel')
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