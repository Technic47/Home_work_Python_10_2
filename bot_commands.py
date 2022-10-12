from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
from keyboards import calculus
from aiogram import Bot, types
from logger import Logger
import numexpr as ne
import config

bot = Bot(config.TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())

log = Logger()


@dp.message_handler(commands=['help'])
async def help_me(message: types.Message):
    with open('READ_ME.txt', 'r') as file:
        read_me = file.readlines()
        for line in read_me:
            await bot.send_message(message.from_user.id, line)


@dp.message_handler(commands=['start', 'calc'])
async def new_db(message: types.Message):
    global value, old_value
    await bot.send_message(message.from_user.id, 'Lets start!', reply_markup=calculus)


@dp.callback_query_handler(lambda callback_query: True)
async def callback_func(query):
    global value, old_value
    data = query.data
    old_value = value

    match data:
        case '=':
            try:
                result = ne.evaluate(value)
                value = str(result)
                log.log(query.from_user.username, old_value, value)
            except:
                value = 'Error!'
        case 'C':
            value = ''
        case '<=':
            if value != '':
                value = value[:len(value) - 1]
        case _:
            value += data

    if (value != old_value and value != '') or ('0' != old_value and value == ''):
        if value == '':
            await bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id, text='0',
                                        reply_markup=calculus)
            old_value = '0'
        else:
            await bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id, text=value,
                                        reply_markup=calculus)
            old_value = value
    if value == 'Error!':
        value = ''


@dp.message_handler()
async def echo_send(message: types.Message):
    await message.answer(message.text)


value = ''
old_value = ''
