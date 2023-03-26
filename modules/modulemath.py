import math
from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from modules import config, keyboards

storage = MemoryStorage()
bot = Bot(token=config.TELEGRAM_API_KEY, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)

#[Код Калькулятора] =================================================================

async def calculator(message: types.Message):
    global value_calculator
    if value_calculator != '':
        await bot.send_message(message.chat.id, text= value_calculator, reply_markup = keyboards.calc_button_class())
    else:
        await bot.send_message(message.chat.id, 'Введите пример,который требуется решить', reply_markup = keyboards.calc_button_class())

async def callback_calculator_func(callback: types.CallbackQuery):
    global value_calculator
    data = callback.data
    if data == 'clear':
        await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, text='0', reply_markup=keyboards.calc_button_class())

    elif data == 'tgs':
        try:
            await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, text=math.tan(float(value_calculator)), reply_markup=keyboards.calc_button_class())
        except:
            await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, text='Произошла ошибка', reply_markup=keyboards.calc_button_class())

    elif data == 'step':
        try:
            await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, text=math.pow(float(value_calculator), 2), reply_markup=keyboards.calc_button_class())
        except:
            await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, text='Произошла ошибка', reply_markup=keyboards.calc_button_class())

    elif data == '=':
        value_calculator = str( eval(value_calculator) )
        await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, text=value_calculator, reply_markup=keyboards.calc_button_class())

    else:
        value_calculator += data
        await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, text=value_calculator, reply_markup=keyboards.calc_button_class())

#[Регистр переменных] =================================================================
value_calculator = ''

#[Регистр Хандлеров] =================================================================
def register_handlers(dp : Dispatcher):
    dp.register_message_handler(calculator, text='Калькулятор')
    dp.register_message_handler(calculator, commands=['calculator'])
    dp.register_callback_query_handler(callback_calculator_func,text=['step', 'tgs', 'clear', '7', '1', '2', '3', '0', '=', '+', '6', '5', '4', '8', '9', '*', '/', '-'])