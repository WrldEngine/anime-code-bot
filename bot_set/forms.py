from aiogram.dispatcher.filters.state import State, StatesGroup

class SetCodeForm(StatesGroup):
	name = State()
	source = State()

class FindCodeForm(StatesGroup):
	code = State()

class PostAdsForm(StatesGroup):
	post = State()
	post_caption = State()