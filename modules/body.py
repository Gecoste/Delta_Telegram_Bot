import os #Модуль для работы с операционной сис-мой
import logging #Модуль для ведения журнала логов
from google.cloud import dialogflow #Модуль DialogFlow
from aiogram import types, Bot, Dispatcher, executor
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup
from modules import config, keyboards, weather, basedate, generate
import requests, json
from bs4 import BeautifulSoup as BS
import wikipedia
from googletrans import Translator
import qrcode
import pyjokes

#[Регистр классов состояния] =================================================================
class Weather(StatesGroup):
    weth = State() # Задаем состояние

class Search(StatesGroup):
    srch = State() # Задаем состояние
    select = State()

class Support(StatesGroup):
    select_reason = State() # Задаем состояние

class Translate_text_state(StatesGroup):
    select_text_in = State() # Задаем состояние

class qrcode_text_state(StatesGroup):
    text_for_qrcode = State() # Задаем состояние

#[Основные переменные] =================================================================

logging.basicConfig(level=logging.INFO) #Логгирование на уровне INFO
storage = MemoryStorage()
bot = Bot(token=config.TELEGRAM_API_KEY, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)
translator = Translator()
bd = basedate.BASADATA()

#[/start] =================================================================

async def send_welcome(message: types.Message):
    if bd.find_user_table(id=message.from_user.id) is None:
        await bot.send_message(message.chat.id,
"""
Привет!
Я готова к работе.
Давай пообщаемся?

Автор: @raizyxadev
""", reply_markup= keyboards.start_button_class())
    else:
        await bot.send_message(chat_id=message.chat.id, text='''
        Ого! Ты получается мой новый друг? 
        Мне очень приятно с тобой пообщаться, но давай сначала пройдем регистрацию.
        Напиши мне свое ФИО (например: Иванов Иван Иванович), если оно не существует в моем списке, то я не смогу тебя зарегистрировать :(
        ''')

#[Прогноз погоды] =================================================================

async def send_weather(message: types.Message):
    msg = await bot.send_message(message.chat.id, "Введите название города, чтобы продолжить")
    await Weather.weth.set() # Устанавливаем состояние

async def print_weather(message: types.Message, state: FSMContext):
    await state.update_data(weth=message.text)
    data = await state.get_data()
    dating = weather.weather(data['weth'], config.WEATHER_API_KEY)
    try:
        msg = await bot.send_message(message.chat.id, f"""Сейчас в городе {data['weth']} 
        | Текущая температура: {dating[1]} °C
        | Ощущается как {dating[3]} °C
        | Мин. температура {dating[4]} °C
        | Ожидается {dating[0]} 
        | Скорость ветра {dating[2]} м/с""")
        await state.finish() # Выключаем состояние
    except:
        await bot.send_message(message.chat.id, 'Произошла непредвидимая ошибка, попробуйте снова написать ваш запрос!)')
 
#[Профиль участника] =================================================================

async def profile(message: types.Message):

    await bot.send_message(message.chat.id, f"""
    Профиль:

    ID: {message.from_user.id}
    ФИО: {message.from_user.full_name}
    Ваша должность: ученик
    Ваш класс: None
    Вы состоите в кружке: None
    
    <code> DELTA PRODUCT </code>
    """)

async def helps(message: types.Message):
    await bot.send_message(message.chat.id, """
    <code> DELTA | Помощь по командам </code>
    
    <b>1. /start </b> - Откроется основное меню, в котором вы увидите кнопки (Технической поддержки,Школьное меню, Ваш профиль и тд)
    <b>2. /weather </b> - Расскажу вам о погоде на данный момент в любом городе мира (Я реагирую не только на команду, но и на текст: Погода, Покажи погоду)
    <b>3. /profile </b> - Покажу вам ваш профиль, в котором отображается статус, класс и многое другое (Я реагирую не только на команду, но и на текст: Профиль, Покажи профиль)
    <b>4. /calculator </b> - Открою для вас калькулятор с огромным функционалом (Я реагирую не только на команду, но и на текст: Калькулятор)
    <b>5. /translate </b> - Переведу ваш текст на доступные языки: Английский, Русский, Китайский (Я реагирую не только на команду, но и на текст: )
    """)

#[Парсинг бразуера,ютуба на наличие информации] =================================================================
async def search_info(message: types.Message):
    await bot.send_message(message.chat.id, text='Расскажите пожалуйста, что мне нужно для вас найти?')
    await Search.srch.set()
    
async def catalog_search_info(message: types.Message, state: FSMContext):
    await state.update_data(srch=message.text)
    data = await state.get_data()

    if config.BAD_WORDS & set(message.text.lower().split()):
        await bot.send_message(message.chat.id, text='Простите,но я не могу выдать вам результаты вашего запроса,т.к в ней встретились плохие слова и показ такой информации запрещен,по Конституции вашей страны: ' + ', '.join(config.BAD_WORDS & set(message.text.lower().split())))
    else:
        """youtube_href = requests.get('https://www.youtube.com/results?search_query=' + data['srch'])
        soup = BS(youtube_href.content, 'html.parser')
        result = soup.find_all('a', id='video_title')
        for link in result:
            url = 'https://www.youtube.com' + link['href']
            bot.send_message(message.chat.id, text=f'Ссылка на видео: {url}')"""
        wikipedia.set_lang('ru')
        try:
            msg = wikipedia.search(f"{data['srch']}", results = 4)
        except:
            pass
        if not msg:
            await bot.send_message(message.chat.id, text='Простите,но я не смогла найти на Wikipedia нужную для вас информацию,попробуйте правильно составить запрос и напишите его мне:)')  
        else:
            button = []
            for words in config.BAD_WORDS:
                for item in msg:
                    if words in item:
                        msg.remove(item)
            for i in range(len(msg)):
                button.append([types.InlineKeyboardButton(text=msg[i], callback_data=f'search_wik{i}')])
            wikipedia_button_search = types.InlineKeyboardMarkup(inline_keyboard=button)
            await Search.select.set()
            await bot.send_message(message.chat.id, text='Выберите каталог,о котором хотите узнать информацию', reply_markup=wikipedia_button_search)

async def select_search_info(message: types.Message, state: FSMContext):
    await state.update_data(select=message.text)
    data = await state.get_data()
    msg = wikipedia.summary(data['select'], sentences=4)
    await bot.send_message(message.chat.id, text=f'На Wikipedia сказано: {msg}')
    await state.finish()
    
#[Реакция на нового пользователя(Для сообществ)] =================================================================
async def new_added_user(message: types.Message):
    for user in message.new_chat_members:
        await message.reply(f"Приветсвую тебя, {user.full_name}. Чтобы познакомиться со мной, напиши мне <b>/start</b>") 

#[Реакция на стикеры] =================================================================
async def reaction_sticker(message: types.Message):
        await message.reply(f"Интересный стикер,я его сохраню себе,ты не против?)")
        
#[Техническая поддержка] =================================================================
async def technical_support(message: types.Message):
    await bot.send_message(message.chat.id, text='Выберите из списка,зачем вам требуется обратиться в техническую поддержку', reply_markup=keyboards.support()) 

async def callback_support_func(callback: types.CallbackQuery):
    data = callback.data
    global reason
    if data == 'sugidea':
        reason = 'Предложение идеи'
        await Support.select_reason.set()
        await bot.send_message(callback.message.chat.id, 'Напишите текст,чтобы вы хотели добавить или имзенить во мне, а я передам его разработчику. Спасибо за ваше обращение. Оно сделает меня лучше:)')
    elif data == 'techcancel':
        await bot.send_message(callback.message.chat.id, 'Вы отменили запрос, на написание в техническую поддержку, но если что, я буду на готове')
        pass
    else:
        reason = 'Написал об ошибке'
        await Support.select_reason.set()
        await bot.send_message(callback.message.chat.id, 'Распишите подробно ошибку,которая у вас появилась,я передам разработчику, для быстрого исправления. Спасибо за ваше обращение. Оно сделает меня лучше:)')

async def result_support_info(message: types.Message, state: FSMContext):
    await state.update_data(select_reason=message.text)
    global reason
    data = await state.get_data()
    await bot.send_message(config.DEVELOPER, text=f"""
    Пользователь {message.from_user.mention} отправил вам сообщение в технический раздел:
    | Причина: {reason}
    | Сообщение: {data['select_reason']}
    """)
    await bot.send_message(message.chat.id, text='Я отправила ваше сообщение в технический раздел')
    await state.finish()

#[Перевод фраз,текста] =================================================================
async def translate_text_input(message: types.Message):
    await Translate_text_state.select_text_in.set()
    await bot.send_message(message.chat.id, text=f'{message.from_user.mention}, введите текст, который мне требуется перевести на другой язык')

async def transtale_text_load(message: types.Message, state: FSMContext):
    await state.update_data(select_text_in=message.text)
    data_text_result = await state.get_data()
    global result_translate_text
    result_translate_text = data_text_result['select_text_in']
    await bot.send_message(chat_id=message.chat.id, text=f'{message.from_user.mention}, выберите язык, на который вы хотите перевести текст', reply_markup=keyboards.button_languages())
    await state.finish()

async def callback_translate_func(callback: types.CallbackQuery):
    data = callback.data
    global result_translate_text
    await bot.send_message(chat_id=callback.message.chat.id, text='Вот что у меня получилось: ' + translator.translate(text=f'{result_translate_text}', dest=f'{data}').text)

#[Создание qrcode] =================================================================
async def form_qrcode(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text=f'{message.from_user.mention}, напишите текст или URL, который мне требуется перевести в QRCODE')
    await qrcode_text_state.text_for_qrcode.set()

async def result_qrcode(message: types.Message, state: FSMContext):
    await state.update_data(text_for_qrcode=message.text)
    data = await state.get_data()
    qr = qrcode.make(data).save('qrcode.png')
    await bot.send_photo(chat_id=message.chat.id, caption=f'{message.from_user.mention}, чуть ниже я прикрепила изображение QRcode, которого вы попросили сделать', photo=open('qrcode.png', 'rb'))
    os.remove('qrcode.png')
    await state.finish()

#[Генератор анекдотов] =================================================================

async def generate_jokes(message: types.Message):
    joke = pyjokes.get_joke()
    await bot.send_message(chat_id=message.chat.id, text=f"{message.from_user.mention}, я сгенерировала для вас очень интересный анекдот: {translator.translate(text=joke, dest='ru').text}")

#[Панель администратора] =================================================================
async def open_admin_panel(message: types.Message):
    if str(message.from_user.id) in config.ADMIN_USER:
        await bot.send_message(chat_id=message.chat.id, text=f"{message.from_user.mention}, вы зашли в панель администратора", reply_markup=keyboards.admin_button_class())

#[Расписание класса, столовой] =================================================================
async def check_school_reason(message: types.Message):

    await bot.send_message(chat_id=message.chat.id, text=f'Сейчас у вас по расписанию урок в кабинете . Расписание на завтрашний день')

#[Регистр переменных] =================================================================

reason = ''
result_translate_text = ''

#[Безопасный маршрут в школу] =============================================================+

async def generate_school_road(msg: types.Message):
    start = types.ReplyKeyboardMarkup()
    kb = types.KeyboardButton('Отправить адрес', request_location=True)
    start.add()

    await bot.send_message(chat_id=msg.chat.id, text='Место мое', reply_markup=start)

#[Регистр Хандлеров] =================================================================
def register_handlers(dp : Dispatcher):
    dp.register_message_handler(send_welcome, commands=['start'])
    dp.register_message_handler(send_weather, commands=['weather'])
    dp.register_message_handler(send_weather, text=['Погода', 'погода'])
    dp.register_message_handler(profile, commands=['profile'])
    dp.register_message_handler(profile, text=['📰 Профиль', 'Профиль'])
    dp.register_message_handler(helps, text= ['🔗 Помощь', 'Помощь', 'помощь'])
    dp.register_message_handler(helps, commands=['help'])
    dp.register_message_handler(print_weather, state=Weather.weth)
    dp.register_message_handler(search_info,text='Поиск информации')
    dp.register_message_handler(generate_jokes, text=['Анекдот', 'Напиши Анекдот'])
    dp.register_message_handler(catalog_search_info, state=Search.srch)
    dp.register_message_handler(select_search_info, state=Search.select)
    dp.register_message_handler(new_added_user, content_types=["new_chat_members"])
    dp.register_message_handler(reaction_sticker, content_types=["sticker"])
    dp.register_message_handler(technical_support, text= ['🎧 Техническая поддержка', 'техническая поддержка'])
    dp.register_message_handler(translate_text_input, text=['Переведи', 'переведи текст'])
    dp.register_message_handler(form_qrcode, text=['qrcode', 'генерация qrcode'])
    dp.register_callback_query_handler(callback_support_func, text=['sugidea', 'wrerror', 'techcancel'])
    dp.register_message_handler(result_support_info, state=Support.select_reason)
    dp.register_message_handler(transtale_text_load, state=Translate_text_state.select_text_in)
    dp.register_message_handler(result_qrcode, state=qrcode_text_state.text_for_qrcode)
    dp.register_callback_query_handler(callback_translate_func, text=['ru', 'en', 'fr'])
    dp.register_message_handler(open_admin_panel, text=['админ'])
    dp.register_message_handler(check_school_reason, text=['💻Учебный процесс'])
    dp.register_message_handler(generate_school_road, text=['маршрут'])