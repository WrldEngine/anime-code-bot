import asyncio
import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from bot_set.forms import SetCodeForm, FindCodeForm, PostAdsForm
from bot_set.format_table import print_pretty_table
from bot_set.models import Users, AnimeCode
from bot_set.buttons import *

TOKEN = ''

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

def set_admin(telegram_id):
	admin = Users.get_or_none(Users.telegram_id == telegram_id)

	if admin:
		admin.is_admin = True
		admin.save()

@dp.message_handler(commands=['start'])
async def start(message):
	telegram_id = message.from_user.id
	username = message.from_user.username

	info = f'Здравствуйте, <b>{message.from_user.first_name}</b>'

	user = Users.get_or_none(Users.telegram_id == telegram_id)
	if not user:
		user = Users(telegram_id=telegram_id, username=username)
		user.save()

		print(f"User: {username}, id: {telegram_id}")
	else:
		info = f'Здравствуйте еще раз, <b>{message.from_user.first_name}</b>'
	
	await message.answer(info, parse_mode='html', reply_markup=start_buttons())

@dp.message_handler(commands=['admin'])
async def admin(message):
	user_is_admin = Users.get_or_none(Users.telegram_id == message.from_user.id).is_admin

	if user_is_admin:
		await message.answer('Админка', reply_markup=admin_buttons())
	else:
		await message.answer('Вы не админ')

@dp.message_handler()
async def listen(message):
	if message.text == 'Поиск по коду':
		await message.answer('Введите код')
		await FindCodeForm.code.set()

	if message.text == 'Реклама':
		count = Users.select().count()
		await message.answer(f"Количество пользователей: {count}\nПисать по рекламе @Callistodev1")

@dp.callback_query_handler(lambda c: c.data == 'show_users')
async def proccess_callback_show_users(callback_query):
	text = [['id', 'telegram_id', 'username', 'date', 'is_admin']]

	for user in Users.select():
		text.append([str(user.id), str(user.telegram_id), str(user.username), str(user.date), str(user.is_admin)])

	await bot.answer_callback_query(callback_query.id)
	await bot.send_message(callback_query.from_user.id, f'<code>{print_pretty_table(text)}</code>', parse_mode='html')

@dp.callback_query_handler(lambda c: c.data == 'show_anime')
async def proccess_callback_show_anime(callback_query):
	text = [['code', 'name', 'source']]

	for anime in AnimeCode.select():
		text.append([str(anime.code), str(anime.name), str(anime.source)])

	await bot.answer_callback_query(callback_query.id)
	await bot.send_message(callback_query.from_user.id, f'<code>{print_pretty_table(text)}</code>', parse_mode='html')

@dp.callback_query_handler(lambda c: c.data == 'post_ads')
async def proccess_callback_post_ads(callback_query):
	await bot.answer_callback_query(callback_query.id)
	await bot.send_message(callback_query.from_user.id, 'Отправьте пост')

	await PostAdsForm.post.set()

@dp.callback_query_handler(lambda c: c.data == 'set_code')
async def proccess_callback_set_code(callback_query):
	await bot.answer_callback_query(callback_query.id)
	await bot.send_message(callback_query.from_user.id, 'Введите название аниме')

	await SetCodeForm.name.set()

@dp.message_handler(state='*', commands=['cancel'])
async def cancel(message, state):
	await state.finish()
	await message.reply('Отменено')

@dp.message_handler(state=PostAdsForm.post, content_types=types.ContentType.PHOTO)
async def post_ads(message, state):
	async with state.proxy() as data:
		data['post'] = message.photo[-1]
		data['caption'] = message.caption

	photo_id = data['post'].file_id
	caption = data['caption']

	for user in Users.select():
		await bot.send_photo(user.telegram_id, photo=photo_id, caption=caption)

@dp.message_handler(state=SetCodeForm.name)
async def set_code_name(message, state):
	async with state.proxy() as data:
		data['name'] = message.text

	await message.answer('Теперь введите источник')
	await SetCodeForm.next()

@dp.message_handler(state=SetCodeForm.source)
async def set_code_source(message, state):
	async with state.proxy() as data:
		data['source'] = message.text

		anime = AnimeCode(name=data['name'], source=data['source'])
		anime.save()

	await message.reply(f'Anime: {anime.name}, Code: {anime.code}, Source: {anime.source}', disable_web_page_preview=True)
	await state.finish()

@dp.message_handler(lambda message: not message.text.isdigit(), state=FindCodeForm.code)
async def procces_findcode_failed(message):
	await message.reply('Код должен содержать числовой формат')

@dp.message_handler(state=FindCodeForm.code)
async def find_code(message, state):
	async with state.proxy() as data:
		data['code'] = message.text

		anime = AnimeCode.get_or_none(AnimeCode.code == int(data['code']))
		if anime:
			await message.answer(
				f'Аниме: <code>{anime.name}</code>\nКод: {anime.code}\nИсточник: {anime.source}',
				parse_mode='html',
				disable_web_page_preview=True
			)
		else:
			await message.answer(f'Такой код не найден')

	await state.finish()

if __name__ == '__main__':
	Users.create_table()
	AnimeCode.create_table()
	executor.start_polling(dp, skip_updates=True)