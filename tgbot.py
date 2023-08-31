import logging
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from config import BOT_API_TOKEN

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def introduction(message: types.Message):
    await message.answer("<b>Welcome to the technical support bot</b>",
                         parse_mode="html")