from aiogram import Bot, Dispatcher, executor, types

from token import TOKEN

import logging

from aiogram.types import Message

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")


@dp.message_handler()
async def echo(message: Message):
    await message.answer(message.text + " halloooo")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)