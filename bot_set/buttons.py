from aiogram import types

def start_buttons():
	add_buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)
	find_code = types.KeyboardButton(text='Поиск по коду')
	ads = types.KeyboardButton(text='Реклама')
	add_buttons.row(find_code, ads)

	return add_buttons

def admin_buttons():
	add_buttons = types.InlineKeyboardMarkup(row_width=1)
	show_users = types.InlineKeyboardButton(text='Показать пользователей', callback_data='show_users')
	set_code = types.InlineKeyboardButton(text='Установить код', callback_data='set_code')
	show_anime = types.InlineKeyboardButton(text='Список аниме', callback_data='show_anime')
	post_ads = types.InlineKeyboardButton(text='Запостить рекламу', callback_data='post_ads')
	add_buttons.add(show_users, set_code, show_anime, post_ads)

	return add_buttons