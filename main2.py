from my_token import TOKEN

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import Message
from random import randint
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
searching = ''
connected_users = []
talking_users = dict(
    
)


@dp.message_handler(commands=['start', 'help'], state='*')
async def send_welcome(message: types.Message, state: FSMContext):
    """This handler will be called when user sends /start or /help command"""
    await message.answer("Hi!\nI'm EchoBot!\nPowered by aiogram.\nPlease, say your name")
    await state.set_state("q1")


@dp.message_handler(commands=['online'], state='*')
async def send_welcome(message: types.Message, state: FSMContext):
    await message.answer(f"There is {len(connected_users)} online.")


@dp.message_handler(commands=['find'], state='*')
async def find(message: Message, state: FSMContext):
    global searching, talking_users
    if searching == '' or searching == message.from_user.id:
        searching = message.from_user.id
        await message.answer('Waiting...')
    else:
        await message.answer('Connected!')
        await bot.send_message(searching, 'Connected!')
        talking_users[message.from_user.id] = searching
        talking_users[searching] = message.from_user.id
        await state.set_state('talking')
        target_state = dp.current_state(chat=searching, user=searching)
        await target_state.set_state('talking')
        searching = ''

@dp.message_handler(state='talking')
async def find(message: Message, state: FSMContext):
    sending = talking_users[message.from_user.id]
    await bot.send_message(sending, message.text)


@dp.message_handler(state="q1")
async def process_name(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data({"name": name})
    await state.set_state("q2")
    await message.answer("Say your age")


@dp.message_handler(state="q2")
async def process_age(message: types.Message, state: FSMContext):
    age = message.text
    if age.isdigit():
        await state.update_data({"age": int(age)})
        await state.set_state("echo")
        await message.answer("Now I am echo-bot!")
        connected_users.append(message.from_user.id)

    else:
        data = await state.get_data()
        await message.answer(f"This is not a number, try another time {data['name']}")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

















if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

