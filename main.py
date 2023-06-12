from my_token import TOKEN
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import Message
from random import randint
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
money = 50000
connected_users = []


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message, state: FSMContext):
    await message.answer("Добро пожаловать в казино!\nДля списка команд пропиши команду /kommands.")
    connected_users.append(message.from_user.id)


@dp.message_handler(commands=['kommands'])
async def kommands(message: types.Message):
    await message.answer('Список команд:'
                         '\n/play - Поставить на рулетку'
                         '\n/me - Информация о себе'
                         '\n/maths - Решить пример и получить деньги'
                         '\n/myid - Узнать свой ID')
@dp.message_handler(commands=['me'], state='*')
async def me(message: types.Message, state: FSMContext):
    global money
    await message.answer(f'На счету у тебя ${money}')

@dp.message_handler(commands=['myid'], state='*')
async def myid(message: types.Message, state: FSMContext):
    await message.answer(f'Твой ID:{message.from_user.id}')



@dp.message_handler(commands=['maths'], state='*')
async def maths(message: types.Message, state: FSMContext):
    a = randint(10, 100)
    b = randint(10, 100)
    c = randint(1, 2)
    if c == 1:
        await message.answer(f'Реши пример:{a}+{b}')
        answer = a + b
    else:
        await message.answer(f'Реши пример:{a}-{b}')
        answer = a - b

    await state.update_data({"answer": answer})

    await state.set_state("q1")


@dp.message_handler(state='q1')
async def maths2(message: types.Message, state: FSMContext):
    global money

    d = message.text
    data = await state.get_data()
    answer = data["answer"]
    if answer == int(d):
        get = randint(3000, 5000)
        await message.answer(f'Правильно! Ты получаешь ${get}')
        money += get
    else:
        await message.answer(f'Неправильно! Правильный ответ: {answer}')






if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
