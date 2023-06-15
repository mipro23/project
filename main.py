from collections import defaultdict
from random import randint

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

from my_token import TOKEN

# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
play_commands = ["красное", "черное", "большое", "маленькое", '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
                 '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27',
                 '28', '29', '30', '31', '32', '33', '34', '35', '36']
red = [1, 3, 5, 7, 9, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
admins = [1590722856]
users: dict[int, dict] = defaultdict(dict)
used_promo_IAMATESTER = []
used_promo_MATHSISNOTWORKING = []


@dp.message_handler(commands=['start'], state='*')
async def send_welcome(message: types.Message, state: FSMContext):
    if message.from_user.id in admins:
        await message.answer("Добро пожаловать, админ!\nДля начала введи свое имя.")
        await state.set_state('admin_start')
    else:
        await message.answer("Добро пожаловать в казино!\nДля начала введи свое имя.")

        await state.set_state('start')


@dp.message_handler(state='start')
async def send_welcome2(message: types.Message, state: FSMContext):
    name = message.text
    user_id = message.from_id
    users[user_id]['money'] = 50000
    users[user_id]['name'] = name
    await message.answer(f'Регистрация успешно пройдена, {name}! Для списка команд напиши /commands.')
    await state.reset_state(with_data=False)


@dp.message_handler(state='admin_start')
async def send_welcome2(message: types.Message, state: FSMContext):
    name = message.text
    user_id = message.from_id
    users[user_id]['money'] = 1000000000000
    users[user_id]['name'] = name
    await message.answer(f'Регистрация успешно пройдена, {name}! Для списка команд напиши /commands.')
    await state.set_state('admin')


@dp.message_handler(commands=['commands'], state='admin')
async def commands_a(message: types.Message):
    await message.answer('Список команд для админа:'
                         '\n/write - Оправить сообщение пользователю'
                         '\n/check - Посмотреть балланс игрока'
                         '\n/online - Посмотреть список игроков'
                         )


@dp.message_handler(commands=['online'], state='admin')
async def write(message: types.Message, state: FSMContext):
    for user_id, user in users.items():
        await message.answer(
            f'Ник игрока: {user["name"]}   На счету у него ${user["money"]}\n    Его ID:{user_id}')


@dp.message_handler(commands=['write'], state='admin')
async def write(message: types.Message, state: FSMContext):
    await message.answer('Введи ID пользователя')
    await state.set_state('message_a')


@dp.message_handler(state='message_a')
async def write2(message: types.Message, state: FSMContext):
    global a
    a = message.text
    await message.answer('Введи сообщение')
    await state.set_state('message_a2')


@dp.message_handler(state='message_a2')
async def write3(message: types.Message, state: FSMContext):
    b = message.text
    await bot.send_message(a, 'Сообщение от админа:' + b)
    await message.answer('Сообщение успешно отправлено!')
    await state.set_state('admin')


@dp.message_handler(commands=['check'], state='admin')
async def write(message: types.Message, state: FSMContext):
    await message.answer('Введи ID пользователя')
    await state.set_state('check')


@dp.message_handler(state='check')
async def write3(message: types.Message, state: FSMContext):
    b = int(message.text)
    await message.answer(f'Баланс: {money_list[int(b)]}')
    await state.set_state('admin')


@dp.message_handler(commands=['commands'], state='*')
async def commands(message: types.Message):
    await message.answer(
        'Список команд:\n/play - Поставить на рулетку\n/me - Информация о себе\n/maths - Решить пример и получить деньги\n/channel - Получить ссылку на канал\n/promo - Ввести промокод\n/error - Отправить сообщение в техподдержку\n/pay - Перевод денег другому игроку')


@dp.message_handler(commands=['me'], state='*')
async def me(message: types.Message, state: FSMContext):
    user = users[message.from_id]
    await message.answer(
        f'Твой ник: {user["name"]}\nНа счету у тебя ${user["money"]}\nТвой ID:{message.from_user.id}')


@dp.message_handler(commands=['error'], state='*')
async def error(message: types.Message, state: FSMContext):
    await message.answer('Напиши сообщение')
    await state.set_state('message')


@dp.message_handler(commands=['pay'], state='*')
async def pay(message: types.Message, state: FSMContext):
    await message.answer('Напиши ник или ID игрока, которому хочешь перевести деньги:')
    await state.set_state('pay')


@dp.message_handler(state='pay')
async def pay2(message: types.Message, state: FSMContext):
    name = message.text
    target_id = None
    if name.isdigit():
        target_id = int(name)
    else:
        for user_id, user in users.items():
            if user['name'] == name:
                target_id = user_id

    if target_id:
        await message.answer('Введи сумму перевода:')
        await state.update_data(target_id=target_id)
        await state.set_state("id_pay")
    else:
        await message.answer('Такого ника или ID нет.')
        await state.reset_state(with_data=False)


@dp.message_handler(state='id_pay')
async def pay(message: types.Message, state: FSMContext):
    data = await state.get_data()
    user_id = message.from_id
    user = users[user_id]
    target_id = data["target_id"]
    sm = float(message.text)
    if sm > 0 and sm <= user["money"]:
        user["money"] -= sm
        users[target_id]["money"] += sm
        await message.answer('Деньги переведены успешно!')
        await bot.send_message(target_id,
                               f'Ты получил ${sm} от {user_id}({user["name"]})')
    else:
        if sm > user["money"]:
            await message.answer('Ошибка: Вы хотите перевести больше денег, чем у вас есть.')
        elif sm < 1:
            await message.answer('Ошибка: Вы пытаетесь перевести отрицательное число.')
    await state.reset_state(with_data=False)


@dp.message_handler(state='message')
async def error2(message: types.Message, state: FSMContext):
    text = f"{message.from_user.url}: {message.text}"
    await bot.send_message(admins[0], text)
    await message.answer('Сообщение успешно отправлено! Ждите ответа!')
    await state.reset_state(with_data=False)


@dp.message_handler(commands=['channel'], state='*')
async def channel(message: types.Message, state: FSMContext):
    await message.answer('Ссылка на официальный канал: https://t.me/kasino_bot_news')


@dp.message_handler(commands=['promo'], state='*')
async def channel(message: types.Message, state: FSMContext):
    await message.answer('Введите промокод')
    await state.set_state('promo')


@dp.message_handler(state='promo')
async def prom(message: types.Message, state: FSMContext):
    promo = message.text
    user = users[message.from_id]
    if promo == 'IAMATESTER':
        if message.from_user.id not in used_promo_IAMATESTER:
            await message.answer('Промокод введен! Ты получаешь $400000')
            user["money"] += 400000
            used_promo_IAMATESTER.append(message.from_user.id)
        else:
            await message.answer('Ты уже вводил этот промокод!')
    elif promo == 'MATHSISNOTWORKING':
        if message.from_user.id not in used_promo_MATHSISNOTWORKING:
            await message.answer('Промокод введен! Ты получаешь $1000000')
            user["money"] += 1000000
            used_promo_MATHSISNOTWORKING.append(message.from_user.id)
        else:
            await message.answer('Ты уже вводил этот промокод!')
    else:
        await message.answer('Неправильный промокод!')
    await state.reset_state(with_data=False)


@dp.message_handler(commands=['play'], state='*')
async def play(message: types.Message, state: FSMContext):
    await message.answer(
        'Введи то, на что ты ставишь. Возможные:\nКрасное\nЧерное\nБольшое\nМаленькое\nЛюбое число(например, 12)\nПравила игры: https://ru.wikipedia.org/wiki/%D0%A0%D1%83%D0%BB%D0%B5%D1%82%D0%BA%D0%B0')
    await state.set_state("p1")


@dp.message_handler(state='p1')
async def play(message: types.Message, state: FSMContext):
    answer = message.text.lower()
    if answer in play_commands:
        await message.answer('Введи ставку')
        await state.update_data(answer=answer)
        await state.set_state("p2")
    else:
        await message.answer('Такого нет, попробуй еще раз')


@dp.message_handler(state='p2')
async def play2(message: types.Message, state: FSMContext):
    user = users[message.from_id]
    data = await state.get_data()
    answer = data["answer"]
    cone = message.text
    await message.answer('Крутим рулетку...')
    correct = randint(0, 36)

    if cone.isdigit():
        cone = float(cone)

    if cone <= user["money"]:
        if answer == 'красное' and correct in red:
            await message.answer(f'Поздравляю! Выпало {correct} и ты выиграл ${cone}')
            user["money"] += cone
        elif answer == 'черное' and correct not in red and correct != 0:
            await message.answer(f'Поздравляю! Выпало {correct} и ты выиграл ${cone}')
            user["money"] += cone
        elif answer == 'большое' and correct > 18:
            await message.answer(f'Поздравляю! Выпало {correct} и ты выиграл ${cone}')
            user["money"] += cone
        elif answer == 'большое' and correct < 19 and correct != 0:
            await message.answer(f'Поздравляю! Выпало {correct} и ты выиграл ${cone}')
            user["money"] += cone
        elif answer == correct:
            await message.answer(f'Поздравляю! Выпало {correct} и ты выиграл ${cone * 36}')
            user["money"] += cone
        else:
            await message.answer(f'К сожалению, выпало {correct} и ты проиграл ${cone}')
            user["money"] -= cone
        await state.reset_state(with_data=False)
    else:
        await message.answer('Такого нет, попробуй еще раз')


@dp.message_handler(commands=['maths'], state='*')
async def maths(message: types.Message, state: FSMContext):
    answer = 0
    user = users[message.from_id]
    user["maths"] = answer
    a = randint(10, 100)
    b = randint(10, 100)
    c = randint(1, 2)
    if c == 1:
        await message.answer(f'Реши пример:{a}+{b}')
        answer = a + b
        user["maths"] = answer
    else:
        await message.answer(f'Реши пример:{a}-{b}')
        answer = a - b
        user["maths"] = answer

    await state.set_state("q1")


@dp.message_handler(state='q1')
async def maths2(message: types.Message, state: FSMContext):
    user = users[message.from_id]
    d = message.text
    if user["maths"] == int(d):
        get = randint(3000, 5000)
        await message.answer(f'Правильно! Ты получаешь ${get}')
        user["money"] += get
    else:
        await message.answer(f'Неправильно! Правильный ответ: {user["maths"]}')
    await state.reset_state(with_data=False)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
